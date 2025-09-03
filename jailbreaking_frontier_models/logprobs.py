from typing import Optional

import msgspec


class LogProbs(msgspec.Struct, frozen=True, tag=True):
    prompt_token_strs: list[str]
    prompt_token_logprobs: list[float | None]
    response_token_strs: list[str]
    response_token_logprobs: list[float | None]

    def __sub__(self, other: "LogProbs") -> "LogProbDiff":
        """
        Subtract another LogProbs object from this one to create a LogProbDiff.

        Args:
            other: LogProbs object to subtract from this one

        Returns:
            LogProbDiff object with computed differences (self - other)
        """
        return LogProbDiff.from_logprobs(self, other)

    def sum_response_logp(self) -> float:
        """
        Returns the mean logp of the response tokens. nans are ignored.
        """
        return sum(p for p in self.response_token_logprobs if p is not None)

    def visualize(self) -> None:
        visualize_logprobs(self)

    def trim_response_tokens(self, max_num_tokens: Optional[int] = None) -> "LogProbs":
        """
        Trim the response tokens to a maximum number of tokens.
        """
        if max_num_tokens is None:
            return self

        return LogProbs(
            prompt_token_strs=self.prompt_token_strs,
            prompt_token_logprobs=self.prompt_token_logprobs,
            response_token_strs=self.response_token_strs[:max_num_tokens],
            response_token_logprobs=self.response_token_logprobs[:max_num_tokens],
        )


class LogProbDiff(msgspec.Struct, frozen=True, tag=True):
    logp: LogProbs
    logq: LogProbs
    response_token_strs: list[str]
    response_token_logprobs: list[float | None]

    @classmethod
    def from_logprobs(cls, logp: LogProbs, logq: LogProbs) -> "LogProbDiff":
        """
        Construct a LogProbDiff from two LogProbs objects.

        Args:
            logp: First LogProbs object
            logq: Second LogProbs object (will be subtracted from logp)

        Returns:
            LogProbDiff object with computed differences
        """
        assert len(logp.response_token_strs) == len(
            logq.response_token_strs
        ), f"Token string lists have different lengths: {len(logp.response_token_strs)} vs {len(logq.response_token_strs)}"

        for i, (p_token, q_token) in enumerate(
            zip(logp.response_token_strs, logq.response_token_strs)
        ):
            assert (
                p_token == q_token
            ), f"Token strings differ at position {i}: '{p_token}' vs '{q_token}'"

        diff_logprobs: list[float | None] = []
        for p_logprob, q_logprob in zip(logp.response_token_logprobs, logq.response_token_logprobs):
            if p_logprob is None or q_logprob is None:
                diff_logprobs.append(None)
            else:
                diff_logprobs.append(p_logprob - q_logprob)

        return cls(
            logp=logp,
            logq=logq,
            response_token_strs=logp.response_token_strs,  # Since they're the same
            response_token_logprobs=diff_logprobs,
        )

    def visualize(self) -> None:
        visualize_logprobs(self)


def visualize_logprobs(logprobs: LogProbs | LogProbDiff) -> None:
    """Visualize token logprobs using color gradients in a Jupyter widget.

    For LogProbs: Uses red gradient (transparent for high probability, red for low)
    For LogProbDiff: Uses blue for negative values, red for positive, transparent for 0

    Args:
        logprobs: LogProbs or LogProbDiff object containing token strings and their log probabilities
    """

    try:
        from IPython.display import HTML, display  # type: ignore
    except ImportError:
        print("IPython not found, skipping visualization")
        return

    is_diff = isinstance(logprobs, LogProbDiff)

    if is_diff:
        valid_probs = [p for p in logprobs.response_token_logprobs if p is not None]
        if valid_probs:
            max_abs = max(abs(p) for p in valid_probs)
            if max_abs == 0:
                max_abs = 1
        else:
            max_abs = 1

        def get_color(p: float | None) -> str:
            if p is None:
                return "rgba(0,0,0,0)"
            elif p == 0:
                return "rgba(0,0,0,0)"
            elif p < 0:
                opacity = min(abs(p) / max_abs, 1.0)
                return f"rgba(0,0,255,{opacity})"
            else:
                opacity = min(p / max_abs, 1.0)
                return f"rgba(255,0,0,{opacity})"

    else:
        valid_logprobs = [p for p in logprobs.response_token_logprobs if p is not None]
        if valid_logprobs:
            min_prob = min(valid_logprobs)
            max_prob = max(valid_logprobs)

            def normalize_prob(p: float | None) -> float:
                if p is None:
                    return 0.5
                if max_prob == min_prob:
                    return 0.5
                return (p - min_prob) / (max_prob - min_prob)

        else:

            def normalize_prob(p: float | None) -> float:
                return 0.5

        def get_color(p: float | None) -> str:
            if p is None:
                return "rgba(0,0,0,0)"
            else:
                normalized = normalize_prob(p)
                opacity = 1 - normalized
                return f"rgba(255,0,0,{opacity})"

    html: list[str] = []
    html.append('<div style="font-family: monospace; white-space: pre-wrap;">')

    for token, prob in zip(logprobs.response_token_strs, logprobs.response_token_logprobs):
        color = get_color(prob)

        token = token.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if prob is not None:
            tooltip = f"{prob:.4f}"
        else:
            tooltip = "None"

        html.append(
            f'<span style="background-color: {color}; padding: 2px;" title="{tooltip}">{token}</span>'
        )

    html.append("</div>")

    if is_diff:
        legend = """
        <div style="margin-top: 10px; font-size: 12px;">
            <span style="background-color: rgba(0,0,255,0.8); padding: 2px;">Negative</span>
            <span style="background-color: rgba(0,0,0,0); padding: 2px; border: 1px solid #ccc;">Zero</span>
            <span style="background-color: rgba(255,0,0,0.8); padding: 2px;">Positive</span>
        </div>
        """
    else:
        legend = """
        <div style="margin-top: 10px; font-size: 12px;">
            <span style="background-color: rgba(255,0,0,1); padding: 2px;">Low probability</span>
            <span style="background-color: rgba(255,0,0,0); padding: 2px; border: 1px solid #ccc;">High probability</span>
        </div>
        """

    display(HTML("".join(html) + legend))
