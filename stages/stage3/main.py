import sqlite3
from contextlib import contextmanager

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DB = "readings.db"


@contextmanager
def db():
    """Open the database, hand it over, then always close it."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row      # lets us read columns by name
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                created  TEXT DEFAULT CURRENT_TIMESTAMP,
                sensor   TEXT,
                value    REAL,
                unit     TEXT,
                low      REAL,
                high     REAL,
                severity TEXT
            )
        """)


init_db()


class Reading(BaseModel):
    sensor: str
    value: float
    unit: str
    low: float
    high: float


def classify(value: float, low: float, high: float) -> str:
    if low <= value <= high:
        return "normal"
    margin = (high - low) / 2 or 1
    if value < low - margin or value > high + margin:
        return "critical"
    return "warning"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/readings")
def create_reading(reading: Reading):
    severity = classify(reading.value, reading.low, reading.high)
    with db() as conn:
        cursor = conn.execute(
            "INSERT INTO readings (sensor, value, unit, low, high, severity)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (reading.sensor, reading.value, reading.unit,
             reading.low, reading.high, severity),
        )
        new_id = cursor.lastrowid
    return {"id": new_id, "sensor": reading.sensor,
            "value": reading.value, "severity": severity}


@app.get("/readings")
def list_readings(limit: int = 20):
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]
