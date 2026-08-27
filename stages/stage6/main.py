import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv
load_dotenv()          # read .env BEFORE anything else looks at the environment

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import ai

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
                severity TEXT,
                reason   TEXT,
                action   TEXT
            )
        """)

        # A database created at Stage 4 has no reason or action column.
        # CREATE TABLE IF NOT EXISTS will not add them, so add them here.
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(readings)")}
        for column in ("reason", "action"):
            if column not in existing:
                conn.execute(f"ALTER TABLE readings ADD COLUMN {column} TEXT")


init_db()


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

    margin = (high - low) / 2 or 1      # how far outside counts as "a lot"
    if value < low - margin or value > high + margin:
        return "critical"

    return "warning"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/readings")
def create_reading(reading: Reading):
    # 1. Our own code decides how serious it is. Instant, always correct.
    severity = classify(reading.value, reading.low, reading.high)

    # 2. The AI turns that into a sentence a person can read.
    advice = ai.explain(reading.sensor, reading.value, reading.unit,
                        reading.low, reading.high, severity)

    with db() as conn:
        cursor = conn.execute(
            "INSERT INTO readings (sensor, value, unit, low, high,"
            " severity, reason, action) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (reading.sensor, reading.value, reading.unit, reading.low,
             reading.high, severity, advice.reason, advice.action),
        )
        new_id = cursor.lastrowid

    return {
        "id": new_id,
        "sensor": reading.sensor,
        "value": reading.value,
        "unit": reading.unit,
        "severity": severity,
        "reason": advice.reason,
        "action": advice.action,
    }


@app.get("/readings")
def list_readings(limit: int = 20):
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


# Serve the web page from the "static" folder.
# This line must always be LAST, after every endpoint above it.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
