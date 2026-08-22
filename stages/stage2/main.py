from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Reading(BaseModel):
    """Describes what a valid reading looks like.

    FastAPI checks every incoming request against this. If a field is
    missing or the wrong type, the request is rejected before your code runs.
    """
    sensor: str
    value: float
    unit: str
    low: float
    high: float


def classify(value: float, low: float, high: float) -> str:
    """Decide how serious a reading is. Plain arithmetic, no AI."""
    if low <= value <= high:
        return "normal"
    margin = (high - low) / 2 or 1          # how far outside is "a lot"
    if value < low - margin or value > high + margin:
        return "critical"
    return "warning"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/readings")
def create_reading(reading: Reading):
    severity = classify(reading.value, reading.low, reading.high)
    return {
        "sensor": reading.sensor,
        "value": reading.value,
        "unit": reading.unit,
        "severity": severity,
    }
