# Full-Stack App Deployment with AI APIs & Cloud

**Project Nexus 2026 — Technical Workshop Series**
Workshop 4 of 10 · 31 August 2026

By the end of this guide you will have built a working web application from an
empty folder and put it on the public internet, where anyone can open it.

You will write every line. Nothing is hidden.

---

## What you need before we start

| | |
|---|---|
| **Python 3.10 or newer** | check with `python --version` |
| **A code editor** | VS Code is fine |
| **A terminal** | Command Prompt, PowerShell, or Terminal |
| **A GitHub account** | free, only needed at Stage 6 |

You do **not** need an AI account, an API key, a credit card, or any paid service.

---

## Part 1 — The concepts you need first

This part has no code. It covers the four ideas everything else is built on.

### 1.1 What "full-stack" means

An application that people use over the internet has three parts.

| Part | What it is | Who can see it |
|---|---|---|
| **Frontend** | the page in the visitor's browser | **everyone** |
| **Backend** | your program, running on a server | only you |
| **Data** | where information is stored between visits | only you |

"Full-stack" simply means you are building all three.

The most important line in that table is the top one. Everything the frontend
receives has been given to the visitor to keep. Press `F12` in any browser and
you can read all of it. There is no way to send something to a browser and hide
it.

That single fact decides where your API key is allowed to live. We come back to
it in Stage 4.

### 1.2 Request and response

Every action on the web is the same two steps:

```
   browser  ──── request ────▶  server
   browser  ◀─── response ────  server
```

Opening a page is a request and a response. Pressing a button is a request and a
response. Your job as a backend developer is to write the code that decides what
goes in the response.

### 1.3 Server

A server is a computer that stays switched on, waiting for requests. That is the
whole idea. During Stages 1 to 5 the server is your own laptop. In Stage 6 we
move it to a computer in a data centre so it never turns off.

### 1.4 What we are building

A **sensor triage service**.

Something sends a reading. Your code decides whether it is safe. An AI writes a
short explanation. The result is stored and displayed.

This shape fits every Project Nexus track, because every track measures a number
that has a safe range:

| Track | Example reading | Safe range |
|---|---|---|
| Healthcare | body temperature 39.4 °C | 36.1 – 37.2 °C |
| Healthcare | blood oxygen 88 % | 95 – 100 % |
| Sustainable Solutions | indoor CO₂ 1450 ppm | 400 – 1000 ppm |
| Sustainable Solutions | power draw 4800 W | 0 – 3500 W |
| Global Impact | soil moisture 8 % | 30 – 70 % |
| Global Impact | motor temperature 87 °C | 20 – 60 °C |

Whatever your project measures, the code is the same. Only the numbers change.

---

## Part 2 — Build it

Work in **one folder** the whole way through. Each stage adds to the last.

If you fall behind at any point, the `stages/` folder in this repository contains
a complete working copy of every stage. Copy the one you need and carry on.

### Set up the folder

```bash
mkdir sensor-triage
cd sensor-triage
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

> **What is a virtual environment?**
> A private copy of Python for this project only. Packages you install here do
> not affect your other projects. You will see `(.venv)` at the start of your
> terminal prompt when it is active.

Install what we need:

```bash
pip install "fastapi[standard]" uvicorn python-dotenv anthropic
```

---

## Stage 1 — A server that answers

Create a file called `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

Run it:

```bash
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/health> in your browser. You should see:

```json
{"status":"ok"}
```

**You are now running a web server.** That is the whole thing. Six lines.

> **New term — Endpoint**
> One address your server responds to, and the code that handles it. `/health`
> is an endpoint. An application is a collection of endpoints.

> **New term — `@app.get("/health")`**
> This line, called a decorator, tells FastAPI: when a **GET** request arrives
> for the address `/health`, run the function underneath.

### Now open the free test page

Go to <http://127.0.0.1:8000/docs>.

FastAPI generated an interactive page for your API automatically. You can call
your own endpoint from here. You will use this constantly for the rest of the
workshop — it means you can test the backend before writing any frontend at all.

> **Why is it called a health endpoint?**
> Hosting platforms call an address like this every few seconds to check your
> app is still alive. We will point Render at it in Stage 6. Almost every
> production service has one.

**`--reload` means the server restarts automatically when you save a file.**
Leave it running for the rest of the workshop.

---

## Stage 2 — An endpoint that accepts data

So far the server only talks. Now it needs to listen.

Replace `main.py` with:

```python
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
```

### Test it

Go to <http://127.0.0.1:8000/docs>, find **POST /readings**, click
**Try it out**, and send:

```json
{ "sensor": "motor_temp", "value": 87, "unit": "C", "low": 20, "high": 60 }
```

You get back:

```json
{ "sensor": "motor_temp", "value": 87, "unit": "C", "severity": "critical" }
```

Try a few more. These are the results you should get:

| Reading | Safe range | Result |
|---|---|---|
| 36.8 °C | 36.1 – 37.2 | `normal` |
| 37.4 °C | 36.1 – 37.2 | `warning` |
| 39.4 °C | 36.1 – 37.2 | `critical` |
| 8 % | 30 – 70 | `critical` |

> **New term — GET and POST**
> **GET** asks for something. **POST** sends something. Reading a page is a GET;
> submitting a form is a POST. That is the practical difference.

> **New term — JSON**
> The text format programs use to exchange data. It looks like a Python
> dictionary and works the same way. Your ESP32, your browser, and your Python
> code all speak it, which is why they can talk to each other.

### The validation you got for free

In `/docs`, send `"value": "hot"` instead of a number.

You get back **HTTP 422** and a message naming the bad field. Your `classify`
function never ran. The `Reading` class rejected it first.

> **This matters.** Never trust incoming data. Anyone can send anything to your
> address — a broken sensor, a typo, or someone deliberately probing your
> service. Declaring the shape you expect is how you defend against all three at
> once.

---

## Stage 3 — Store the readings

Right now every reading is forgotten the moment you reply. Let's keep them.

Add these imports at the top of `main.py`:

```python
import sqlite3
from contextlib import contextmanager
```

Add this below the imports:

```python
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
```

Replace `create_reading` and add a new endpoint:

```python
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
```

### Test it

Send two or three readings through `/docs`, then call **GET /readings**. They
are all there, newest first, each with an `id` and a timestamp.

Now stop the server (`Ctrl+C`) and start it again. Call `/readings` once more.
**The data is still there.** A file called `readings.db` appeared in your folder.

> **New term — SQLite**
> A complete database that lives in a single file. No installation, no server,
> no configuration. Perfect for a prototype.

> **Why the question marks?**
> `VALUES (?, ?, ?)` with the values passed separately is called a parameterised
> query. Never build SQL by joining strings together — that is how SQL injection
> attacks work. Always use `?`.

---

## Stage 4 — Connect the AI API

This is the centre of the workshop.

### First, the design decision

Look at what `classify()` already does. It compares numbers. It is instant,
free, correct every time, and you can test it.

**Do not give that job to an AI.** A language model is slower, costs money, and
is measurably worse at it. Tested on a small local model with eight readings,
three runs each, asking only "is this inside the range?":

| Approach | Correct |
|---|---|
| Plain Python arithmetic | **100 %** |
| Small language model | 38 % |
| Larger language model | 83 % |

The larger model classified **87 °C as "normal"** when the safe range was
20 – 60 °C, on two runs out of three.

So we split the work:

- **Your code decides** the severity. It is a fact.
- **The AI explains** what it means, in a sentence a person wants to read.

That is a job code genuinely cannot do, and it is where an AI earns its place.

### Create the `.env` file

Create a file called `.env`:

```
USE_MOCK=true
ANTHROPIC_API_KEY=
CLAUDE_MODEL=claude-haiku-4-5
```

And a file called `.gitignore`:

```
.env
*.db
__pycache__/
.venv/
```

> **New term — Environment variable**
> A setting that lives outside your code, supplied when the program runs. Your
> code reads it, but it is never part of the code itself.

> **New term — API key**
> A long secret string identifying your account with a service. It behaves like
> a bank card with no PIN: whoever holds it can use your account and spend your
> money. There is no second step.
>
> **This is why the key goes in `.env` and never in a `.py` file.** You want to
> share your code. You never want to share your key. Keeping them in separate
> files is what makes that possible — and `.gitignore` is what stops `.env` ever
> being uploaded.

> **And remember Part 1:** the frontend is public. An API key must never be sent
> to the browser under any circumstances. It stays on your server. That is the
> reason your backend exists at all.

### Create `ai.py`

Everything to do with the AI goes in its own file — including the key.

```python
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
```

Three things worth noticing:

1. **`anthropic.Anthropic()` takes no arguments.** It finds `ANTHROPIC_API_KEY`
   in the environment by itself. The key appears nowhere in your code.

2. **`output_format=Advice` guarantees the reply.** The model cannot return a
   paragraph, a refusal, or a differently-named field. You get a validated
   `Advice` object. Without this you would be writing string-parsing code and
   hoping.

3. **`USE_MOCK` lets the whole app run with no key at all.** You can build,
   test, and even deploy before you have an account.

### Wire it into `main.py`

Add at the very top, **above the other imports**:

```python
from dotenv import load_dotenv
load_dotenv()          # read .env BEFORE anything else looks at the environment
```

Add with the other imports:

```python
import ai
```

Add two columns to the table in `init_db()`:

```python
                severity TEXT,
                reason   TEXT,
                action   TEXT
```

> Delete `readings.db` after changing the table, then restart. `CREATE TABLE IF
> NOT EXISTS` will not alter a table that already exists.

Replace `create_reading`:

```python
@app.post("/readings")
def create_reading(reading: Reading):
    # 1. Our own code decides how serious it is. Instant and always correct.
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

    return {"id": new_id, "sensor": reading.sensor, "value": reading.value,
            "severity": severity, "reason": advice.reason, "action": advice.action}
```

### Test it

Send a reading through `/docs`. You now get back a `reason` and an `action`.

With `USE_MOCK=true` those come from the fallback in `ai.py`. **The application
is complete and working without any AI account.**

### Using a real API key

If you have one: put it in `.env` and set `USE_MOCK=false`.

```
USE_MOCK=false
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Restart the server and send another reading. The `reason` is now written by the
model.

**What it costs.** A request like this is roughly 500 tokens in and 150 out.

| Model | Per request | Requests per $5 |
|---|---|---|
| `claude-haiku-4-5` | $0.00125 | about 4,000 |
| `claude-opus-5` | $0.00625 | about 800 |

Set a spending limit on your account before you start, and keep `USE_MOCK=true`
while you are developing.

---

## Stage 5 — The web page

Your backend is finished. Now give it a face.

Create a folder called `static`, and inside it a file `index.html`. The full
file is in `stages/stage5/static/index.html` — copy it in.

Then mount it. Add this import to `main.py`:

```python
from fastapi.staticfiles import StaticFiles
```

And add this line **at the very bottom of the file**, after every endpoint:

```python
# Serve the web page. This line must come LAST, after every endpoint above,
# because it claims every remaining address.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

> **Order matters.** `app.mount("/")` claims every address that has not already
> been claimed. Put it above your endpoints and it will swallow them, and
> `/readings` will start returning your HTML page instead of data.

Open <http://127.0.0.1:8000>. Pick a scenario, press **Send**.

### What the page is actually doing

The important part is these lines:

```javascript
const res = await fetch("/readings", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ sensor, value, unit, low, high }),
});
```

The browser sends a POST to **your own server** — not to the AI company. Your
server adds the key and makes that call on the browser's behalf.

```
   browser  ──▶  your server  ──▶  AI company
                (holds the key)
```

The key never reaches the browser, so a visitor can never take it. This is the
whole reason the backend exists, and it is the single most important structural
idea in the workshop.

---

## Stage 6 — Deploy it to the cloud

Everything so far runs on your laptop. Close the lid and it is gone. Let's put
it on a computer that never turns off.

### Add the two files a server needs

`requirements.txt` — tells the server what to install:

```
fastapi==0.141.1
uvicorn[standard]==0.34.0
pydantic==2.10.4
python-dotenv==1.0.1
anthropic==1.0.0
```

> **Pin the versions.** Writing `fastapi` with no version means the server
> installs whatever is newest on the day it builds. Your app can then break
> weeks later without you changing a single line. Use `pip freeze` to see the
> exact versions you are running.

`render.yaml` — tells Render how to run it:

```yaml
# Render reads this file and sets the whole service up for you.
services:
  - name: sensor-triage
    type: web
    runtime: python
    plan: free                    # no credit card required
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health      # Render calls this to check the app is alive
    envVars:
      - key: USE_MOCK
        value: "true"             # change to "false" once you add a key

      # 'sync: false' means: this setting exists, but its value is typed
      # into the Render dashboard, never written in this file.
      # This file is uploaded to GitHub. A key must never be in it.
      - key: ANTHROPIC_API_KEY
        sync: false
```

Two details to understand:

**`--port $PORT`** — the hosting platform chooses the port and tells your app
through an environment variable. Never hardcode `8000` in production.

**`sync: false`** — `render.yaml` gets uploaded to GitHub. A key written as a
`value:` here would be published exactly as if you had put it in your code.
`sync: false` declares the setting without its value; you type the value into
the dashboard afterwards.

### Upload to GitHub

```bash
git init
git add .
git commit -m "Sensor triage service"
```

**Before you push, check what you are about to upload:**

```bash
git status
```

`.env` must **not** appear. If it does, stop and check `.gitignore`.

> **Why this matters more than it looks.** If a key is ever uploaded, deleting
> it later does not remove it. Git keeps every past version, and anyone who
> clones your repository can read the old one with a single command. The only
> real fix is to go to the provider, delete that key, and create a new one.
> Providers also scan public repositories automatically and disable keys they
> find, usually within minutes.

Create an empty repository on GitHub, then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git branch -M main
git push -u origin main
```

### Deploy

1. Go to [render.com](https://render.com) and sign up with GitHub. No card required.
2. Click **New** → **Blueprint**.
3. Select your repository, then **Apply**.
4. Wait about three minutes while it builds. Errors during this time are normal.
5. You now have a public address, something like
   `https://sensor-triage-xxxx.onrender.com`

Open it on your phone. Send it to someone.

**Your application is on the internet.**

### Add your key in production

`ANTHROPIC_API_KEY` was declared with `sync: false`, so it exists with no value.
In the Render dashboard: **Environment** → set its value → **Save**. Then change
`USE_MOCK` to `false` in `render.yaml` and push.

> Changing `USE_MOCK` in the dashboard will not work, because `render.yaml`
> gives it a value and the file wins. Anything with a `value:` in the file must
> be changed in the file. This surprises people, so remember which of your
> settings live where.

---

## Things you will run into

| What you see | Why | Fix |
|---|---|---|
| First visit takes 30–60 seconds | free servers sleep after 15 minutes idle | open the link yourself before a demo |
| Stored readings vanish after deploying | free servers wipe their disk on each deploy | use a managed database if the data matters |
| `Address already in use` | the old server is still running | `uvicorn main:app --reload --port 8001` |
| New database column missing | `CREATE TABLE IF NOT EXISTS` will not alter an existing table | delete `readings.db` and restart |
| `/readings` returns your HTML page | `app.mount("/")` is above your endpoints | move it to the bottom of the file |
| Everything works but the AI never runs | `USE_MOCK` is still `true` | check `/health` and your environment settings |

---

## Appendix A — Free AI with no account

You can run a small model on your own laptop with [Ollama](https://ollama.com),
at no cost and with no internet connection.

```bash
ollama pull llama3.2:3b
```

Then add a third branch to `explain()` in `ai.py` that posts to
`http://localhost:11434/api/chat`.

**One warning.** `localhost` means *the computer the code is running on*. On
your laptop that is your laptop, and Ollama is there. On a deployed server it is
the server, and Ollama is not there. A local model works for a laptop demo; it
cannot work on free hosting, which offers around 512 MB of memory against the
roughly 4 GB a small model needs.

---

## Appendix B — Making it feel fast

Our `/readings` endpoint waits for the AI before replying. With a fast model
that is fine. With a slow one, the same request can take between 5 and 26
seconds — and the visitor sits and waits.

The professional fix is to reply immediately with the severity, which your code
already computed, and fill in the explanation afterwards:

1. Compute the severity and save the row with `ai_status = "pending"`.
2. Return straight away.
3. Do the AI call in a background task and update the row.
4. Have the page poll until the explanation appears.

FastAPI has `BackgroundTasks` built in for exactly this.

You have seen this pattern already: a messaging app shows your message
instantly with one tick, then updates the delivery status a moment later.

---

## What you built

- A web server with four endpoints
- Input validation that rejects bad data before your code runs
- A database that survives restarts
- An AI integration with the key handled correctly
- A web page that talks to your own backend
- All of it deployed and running on the public internet

Every part of that is reusable. The next application you build has the same
shape.
