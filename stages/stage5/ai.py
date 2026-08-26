"""Everything to do with the AI provider lives in this one file.

It is also the only file that ever touches an API key.

Set AI_PROVIDER in .env to choose. Nothing else in the application changes.
"""
import json
import os

from pydantic import BaseModel, Field

PROVIDER = os.getenv("AI_PROVIDER", "mock").lower()

SYSTEM = (
    "You explain sensor readings to a maintenance engineer. "
    "Be specific and brief. Always mention the measured value."
)


class Advice(BaseModel):
    """The shape of the answer we require, whichever provider produces it."""
    reason: str = Field(description="why the reading is at this level, under 15 words")
    action: str = Field(description="one concrete next step, under 10 words")


# Providers that speak the OpenAI protocol. Only the address and the model
# name differ, which is why one function serves all of them.
OPENAI_COMPATIBLE = {
    "openai":   ("https://api.openai.com/v1",           "OPENAI_API_KEY",   "gpt-4o-mini"),
    "deepseek": ("https://api.deepseek.com/v1",         "DEEPSEEK_API_KEY", "deepseek-chat"),
    "gemini":   ("https://generativelanguage.googleapis.com/v1beta/openai/",
                 "GEMINI_API_KEY",  "gemini-2.0-flash"),
    "groq":     ("https://api.groq.com/openai/v1",      "GROQ_API_KEY",     "llama-3.3-70b-versatile"),
    "ollama":   ("http://localhost:11434/v1",           "OLLAMA_API_KEY",   "llama3.2:3b"),
}


def _prompt(sensor, value, unit, low, high, severity):
    return (
        f"A {sensor} sensor reads {value}{unit}. "
        f"Its safe range is {low}{unit} to {high}{unit}. "
        f"An automatic check rated this {severity}."
    )


def _mock(sensor, value, unit, low, high, severity):
    return Advice(
        reason=f"{value}{unit} against a safe range of {low}-{high}{unit}.",
        action="Set AI_PROVIDER to a real provider for a written answer.",
    )


def _anthropic(sensor, value, unit, low, high, severity):
    """Anthropic's own SDK. output_format guarantees the two fields."""
    import anthropic

    client = anthropic.Anthropic()      # reads ANTHROPIC_API_KEY
    response = client.messages.parse(
        model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        max_tokens=256,
        system=SYSTEM,
        messages=[{"role": "user",
                   "content": _prompt(sensor, value, unit, low, high, severity)}],
        output_format=Advice,
    )
    return response.parsed_output


def _openai_compatible(sensor, value, unit, low, high, severity):
    """OpenAI, DeepSeek, Gemini, Groq and a local Ollama all speak this."""
    from openai import OpenAI

    base_url, key_name, default_model = OPENAI_COMPATIBLE[PROVIDER]
    api_key = os.getenv(key_name) or "not-needed"      # Ollama needs no key
    model = os.getenv(f"{PROVIDER.upper()}_MODEL", default_model)

    client = OpenAI(base_url=base_url, api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        max_tokens=256,
        response_format={"type": "json_object"},       # ask for JSON, not prose
        messages=[
            {"role": "system",
             "content": SYSTEM + ' Reply as JSON: {"reason": "...", "action": "..."}'},
            {"role": "user",
             "content": _prompt(sensor, value, unit, low, high, severity)},
        ],
    )
    return Advice(**json.loads(completion.choices[0].message.content))


def explain(sensor: str, value: float, unit: str,
            low: float, high: float, severity: str) -> Advice:
    """Ask the configured provider to put the reading into words."""
    if PROVIDER == "mock":
        return _mock(sensor, value, unit, low, high, severity)
    if PROVIDER == "anthropic":
        return _anthropic(sensor, value, unit, low, high, severity)
    if PROVIDER in OPENAI_COMPATIBLE:
        return _openai_compatible(sensor, value, unit, low, high, severity)

    raise RuntimeError(
        f"Unknown AI_PROVIDER '{PROVIDER}'. Use one of: "
        f"mock, anthropic, {', '.join(OPENAI_COMPATIBLE)}"
    )
