"""Everything to do with the AI provider lives in this one file.

It is also the only file that ever touches the API key.
"""
import os

import anthropic
from pydantic import BaseModel, Field

# Read settings from the environment. Never write a key into your code.
USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"
MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5")

SYSTEM = (
    "You explain sensor readings to a maintenance engineer. "
    "Be specific and brief. Always mention the measured value."
)


class Advice(BaseModel):
    """The shape of the answer we require.

    Because we hand this to the API, the model is forced to reply with
    exactly these two fields. We never have to parse loose text.
    """
    reason: str = Field(description="why the reading is at this level, under 15 words")
    action: str = Field(description="one concrete next step, under 10 words")


def explain(sensor: str, value: float, unit: str,
            low: float, high: float, severity: str) -> Advice:
    """Ask the AI to put the reading into words."""

    if USE_MOCK:
        return Advice(
            reason=f"{value}{unit} against a safe range of {low}-{high}{unit}.",
            action="Set USE_MOCK=false to get a real AI answer.",
        )

    prompt = (
        f"A {sensor} sensor reads {value}{unit}. "
        f"Its safe range is {low}{unit} to {high}{unit}. "
        f"An automatic check rated this {severity}."
    )

    client = anthropic.Anthropic()      # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.parse(
        model=MODEL,
        max_tokens=256,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        output_format=Advice,           # this is what forces the two fields
    )
    return response.parsed_output
