# Jailbreaking Frontier Models

This repo accompanies the blog post, ["Automatically Jailbreaking Frontier Language Models with Investigator Agents"](https://transluce.org/jailbreaking-frontier-models). 

We provide a reference implementation of the dataset and reward function from our blog post. Please keep in mind that this implementation prioritizes clarity over efficiency, so you may want to optimize it based on your needs. 

We did not include the RL training loop in this release, as it's closely integrated with our internal research infrastructure. That said, we hope this codebase provides a helpful start for anyone interested in training jailbreaking agents or building upon our experiments.

## Dataset

The dataset is located at `data/jailbreak_dataset.jsonl`. The lines have the following format:

```json
{
    "behavior_id": "<unique id for the behavior>",
    "behavior": "<user prompt for the behavior to elicit>",
    "category": "<one of drug/chemical/biological/radiological/nuclear/explosive>",
    "optimizer_target": "<start of an affirmative response, like \"Sure...\" -- this is not used by our investigator agent, but might be useful for other jailbreaking techniques>",
}
```

## Running the reference reward function

### Install dependencies

First install [uv](https://docs.astral.sh/uv/), then run the following to install the dependencies in a virtual environment.

```bash
uv sync
```

### Set up environment variables

Set the `OPENAI_API_KEY` environment variable to your OpenAI API key. Executing the test script below will send a few queries to `gpt-4.1-mini`, which we use as our default judge model.

### Run a test script demonstrating the PRBO reward function

First, host [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) with an OpenAI-compatible endpoint (e.g. vLLM or SGLang) running at an accessible URL, which we will refer to as `http://HOSTNAME:PORT/v1`. Then, run the following command to compute the PRBO reward for a test prompt:

```bash
uv run python examples/reward_fn_computation.py gpt_oss_base_url=http://HOSTNAME:PORT/v1
```

**Warning:** In the paper, we tested many training runs with bonus black-box rewards for attacking various API models (GPT-4.1, GPT-5, Claude Sonnet 4). We do not implement this here, but it is a simple additive bonus to the reward function in this repo (in our training runs, this was a bonus of up to 20 points per model exploited, scaling linearly depending on the response score). We caution that this can get very expensive, especially when sampling responses from flagship reasoning models. **Additionally, since sending many attempted jailbreaks to a production API service may trigger monitors for suspicious activity, it should be done with caution, respecting all applicable policies.**

# Citation

If you reference this work in a publication, please cite:

```bibtex
@misc{chowdhury2025jailbreaking,
  author       = {Chowdhury, Neil and Schwettmann, Sarah and Steinhardt, Jacob},
  title        = {Automatically Jailbreaking Frontier Language Models with Investigator Agents},
  year         = {2025},
  month        = {September},
  day          = {3},
  howpublished = {\url{https://transluce.org/jailbreaking-frontier-models}}
}
```