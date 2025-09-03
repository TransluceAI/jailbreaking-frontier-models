from openai import AsyncOpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from jailbreaking_frontier_models.logprobs import LogProbs
from transformers import PreTrainedTokenizerBase
from tenacity import AsyncRetrying, before_sleep_log, stop_after_attempt, wait_random_exponential
import logging

logger = logging.getLogger(__name__)

async def get_token_logprobs(
    client: AsyncOpenAI,
    tokenizer: PreTrainedTokenizerBase,
    model: str,
    input_token_ids: list[int] | None = None,
    input_messages: list[ChatCompletionMessageParam] | None = None,
    output_token_ids: list[int] | None = None,
    output_text: str | None = None,
) -> LogProbs:
    """Get token-level log probabilities for a response.

    Args:
        client: OpenAI client instance
        model: The model to use
        input_messages: The messages to use
        limiter_fn: The limiter function to use

    Returns:
        LogProbs object containing prompt and response tokens with their logprobs

    WARNING: For vllm, logprobs are not affected by temperature (they assume temperature=1.0). Also, you can't use top_p with logprobs.
    """

    assert (input_token_ids is not None or input_messages is not None) and not (
        input_token_ids is not None and input_messages is not None
    ), "Must provide either input_token_ids or input_messages, but not both"
    assert (output_token_ids is not None or output_text is not None) and not (
        output_token_ids is not None and output_text is not None
    ), "Must provide either output_token_ids or output_text, but not both"

    if input_messages is not None:
        conversation_tokens = tokenizer.apply_chat_template(input_messages, add_generation_prompt=True)  # type: ignore
    elif input_token_ids is not None:
        conversation_tokens = input_token_ids
    else:
        raise ValueError("Must provide either input_messages or input_token_ids")

    assert output_text is not None, "output_text must be provided"

    full_text = tokenizer.decode(conversation_tokens) + output_text

    async for attempt in AsyncRetrying(
        wait=wait_random_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(50),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    ):
        with attempt:
            output = await client.completions.create(
                model=model,
                prompt=full_text,
                max_tokens=1,
                logprobs=1,
                echo=True,
            )

            # Cut off the last tokens, since we sample max_tokens=1 (required for sglang)
            token_strs = output.choices[0].logprobs.tokens[:-1]  # type: ignore
            token_logprobs = output.choices[0].logprobs.token_logprobs[:-1]  # type: ignore

            if token_strs is None or token_logprobs is None:
                raise ValueError("Failed to get logprobs from model")

            suffix_idx = len(conversation_tokens)

            prompt_token_strs = token_strs[:suffix_idx]
            prompt_token_logprobs = list(
                token_logprobs[:suffix_idx]
            )  
            response_token_strs = token_strs[suffix_idx:]
            response_token_logprobs = list(
                token_logprobs[suffix_idx:]
            ) 

            return LogProbs(
                prompt_token_strs=prompt_token_strs,
                prompt_token_logprobs=prompt_token_logprobs,  # type: ignore
                response_token_strs=response_token_strs,
                response_token_logprobs=response_token_logprobs,  # type: ignore
            )

    raise RuntimeError("Failed to get logprobs from model")
