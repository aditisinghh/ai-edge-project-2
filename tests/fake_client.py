"""A scripted stand-in for the Anthropic client, so the agent loop can be tested without an API key."""
from types import SimpleNamespace as NS


def text(t):
    return NS(type="text", text=t)


def tool(name, inp, i):
    return NS(type="tool_use", id=f"tu_{i}", name=name, input=inp)


class FakeClient:
    """Plays back a list of responses; each response is a list of content blocks."""

    def __init__(self, script):
        self.script, self.calls = list(script), []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        blocks = self.script.pop(0)
        return NS(content=blocks, usage=NS(input_tokens=1000, output_tokens=200),
                  stop_reason="tool_use" if any(b.type == "tool_use" for b in blocks) else "end_turn")
