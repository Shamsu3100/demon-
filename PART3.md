# Part 3 — Build it

Five stages. **Each one ends with something you can see on screen**, and each
builds on the last.

Work in **one folder of your own** the whole way through. The `stages/` folder
in this repository holds a complete working copy of every stage — if you fall
behind, copy the one you need and carry on.

---

## Before you start — create the project

### Make the folder

```
mkdir sensor-triage
```

```
cd sensor-triage
```

### Create a virtual environment

```
python -m venv .venv
```

> **What is a virtual environment?**
> A private copy of Python for this project alone. Packages you install here do
> not affect your other projects, and other projects cannot break this one.
>
> It creates a `.venv` folder. You never edit anything inside it.

### Activate it

**Windows:**

```
.venv\Scripts\activate
```

**macOS / Linux:**

```
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. That is how you know it is on.

> **If PowerShell says "running scripts is disabled on this system":** that is
> the Windows trap from Part 0. Run
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`, and try
> again.

**You must activate it every time you open a new terminal.** Forgetting is the
most common cause of "but I installed it already".

### Install what we need

```
pip install "fastapi[standard]" uvicorn python-dotenv anthropic
```

| Package | What it is for |
|---|---|
| `fastapi` | the framework — turns Python functions into web addresses |
| `uvicorn` | the program that actually runs your server |
| `python-dotenv` | reads your settings file, from Stage 5 |
| `anthropic` | talks to the AI service, from Stage 5 |

### Open the folder in VS Code

```
code .
```

The dot means "this folder". If that command does not work, use
**File → Open Folder** and choose `sensor-triage`.

---

# Stage 1 — A server that answers

**Goal:** a program running on your machine that replies to a browser.

### Create `main.py`

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

That is the whole file. Six lines.

### Run it

```
uvicorn main:app --reload
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

> **What does `main:app` mean?**
> The file called `main`, and the object called `app` inside it. If you named
> your file something else, that first word changes.
>
> **What does `--reload` do?**
> Restarts the server automatically whenever you save a file. Leave it running
> for the whole workshop.

### See the result

Open **<http://127.0.0.1:8000/health>**

```json
{"status":"ok"}
```

**You are running a web server.** Something on your machine received a request
and sent back an answer.

### Now open the free test page

Open **<http://127.0.0.1:8000/docs>**

FastAPI generated an interactive page for your API automatically, from your
code. Expand `/health`, click **Try it out**, then **Execute**.

You will use this page for the next two stages. It means you can test your
backend without writing a single line of frontend.

### New terms

> **Endpoint** — one address your server answers, and the code behind it.
> `/health` is an endpoint. An application is a collection of them.

> **Decorator** — the `@app.get("/health")` line. It tells FastAPI: when a GET
> request arrives for this address, run the function underneath.

### Why `/health` in particular

Hosting platforms call an address like this every few seconds to check your
application is alive, and restart it if not. We point Render at it in Part 4.

Almost every production service has one. Yours now does too.

---

# Stage 2 — The page appears

**Goal:** a real web page, that talks to the server you just built.

### Create the folder and file

Inside `sensor-triage`, create a folder called `static`, and inside it a file
called `index.html`.

The full file is at **`stages/stage2/static/index.html`** — copy it. The part
that matters is this:

```javascript
// Ask our own server whether it is alive.
// This is a request; what comes back is a response.
async function checkServer() {
  const box = document.getElementById("status");
  try {
    const res  = await fetch("/health");
    const data = await res.json();
    box.className   = "ok";
    box.textContent = "Connected to your server. It replied: " + data.status;
  } catch (err) {
    box.className   = "fail";
    box.textContent = "Could not reach the server.";
  }
}
checkServer();
```

That is the frontend calling the backend. `fetch("/health")` sends a request to
the same endpoint you tested in `/docs` a moment ago — this time from a page
instead of from a form.

### Serve it

Add one import at the top of `main.py`:

```python
from fastapi.staticfiles import StaticFiles
```

And add this at the **very bottom** of the file:

```python
# Serve the web page from the "static" folder.
# This line must always be LAST, after every endpoint above it.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

> ### This line must be last. Every time.
>
> `app.mount("/")` claims every address that has not already been claimed. Put
> it above your endpoints and it swallows them — `/health` would start
> returning your HTML page instead of data.
>
> FastAPI matches routes in the order you wrote them, and first match wins.
> **Rule to remember: the mount line is always the last line in the file.**

### See the result

Open **<http://127.0.0.1:8000>**

> ### Sensor Triage
> Stage 2 — the page can now talk to your server.
>
> **Connected to your server. It replied: ok**

That sentence is proof of the whole Part 1 model. Your browser made a request.
Your Python code produced a response. The page displayed it.

### What just happened

```
   your browser  ──── GET /health ────▶  your Python code
   your browser  ◀───  {"status":"ok"} ──  your Python code
```

Three separate things you wrote are now working together: a page, a server, and
the connection between them. Everything from here is adding to that.

---

# Stage 3 — Your code decides

**Goal:** send a real reading, and get a verdict back.

### Add the input description

At the top of `main.py`, add this import:

```python
from pydantic import BaseModel
```

Then add this class above your endpoints:

```python
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
```

This is a **description**, not code that runs. You are telling FastAPI the shape
you expect: what the sensor is, what it read, the unit, and the two ends of the
safe range.

### Add the rule

```python
def classify(value: float, low: float, high: float) -> str:
    """Decide how serious a reading is. Plain arithmetic, no AI."""
    if low <= value <= high:
        return "normal"

    margin = (high - low) / 2 or 1      # how far outside counts as "a lot"
    if value < low - margin or value > high + margin:
        return "critical"

    return "warning"
```

Read it aloud: inside the range is normal, a long way outside is critical,
otherwise warning.

The `margin` line is the only clever part. Half the width of the safe range
counts as "a lot" — for a body temperature range of 36.1–37.2 that is about half
a degree; for a motor range of 20–60 it is twenty degrees. **The rule scales
itself to whatever is being measured.**

> **Remember this function.** In Stage 5 we explain why it stays plain
> arithmetic and never becomes the AI's job.

### Add the endpoint

```python
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

Two things are new. `@app.post` rather than `@app.get`, because this request
carries data. And `reading: Reading` in the signature — **that annotation is
what tells FastAPI to read the request body, check it against your class, and
hand you a finished object.** You never parse anything yourself.

### Update the page

Copy `stages/stage3/static/index.html` over your existing file. It adds a
scenario picker, a reading box, and a Send button. The part that matters:

```javascript
// Send the reading to our own server and wait for its answer.
const res = await fetch("/readings", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    sensor: current.sensor, value,
    unit: current.unit, low: current.low, high: current.high,
  }),
});
```

### See the result

Open **<http://127.0.0.1:8000>**, choose a scenario, press **Send**.

> **CRITICAL**
> your code checked: 36.1 ≤ 39.4 ≤ 37.2

Try several. These are the answers you should get:

| Reading | Safe range | Result |
|---|---|---|
| 36.8 °C | 36.1 – 37.2 | `normal` |
| 37.4 °C | 36.1 – 37.2 | `warning` |
| 39.4 °C | 36.1 – 37.2 | `critical` |
| 88 % | 95 – 100 | `critical` |
| 1450 ppm | 400 – 1000 | `critical` |

### Now break it on purpose

Go to `/docs`, find **POST /readings**, click **Try it out**, and send text where
a number belongs:

```json
{ "sensor": "motor_temp", "value": "hot", "unit": "C", "low": 20, "high": 60 }
```

You get back **HTTP 422**, with a message naming the bad field — and **your
`classify` function never ran.** The `Reading` class rejected the request at the
door.

> ### Never trust incoming data
>
> Once your address is public, anyone can send anything to it: a sensor with a
> loose wire, a teammate's typo, or a stranger deliberately probing your
> service.
>
> Declaring the shape you expect defends against all three at once — and you got
> it from one class definition, not from validation code you had to write.
>
> This is a habit worth keeping: **describe your input at the edge of your
> application, every time.**

### New terms

> **JSON** — the text format programs use to exchange data. It looks like a
> Python dictionary and behaves like one. Your browser, your Python code, and a
> microcontroller all speak it, which is why they can talk to each other.

> **GET and POST** — GET asks for something; POST sends something. Reading a
> page is a GET, submitting a form is a POST.

---

# Stage 4 — Remember the readings

Right now every reading is forgotten the moment you reply. Let's keep them.

**Goal:** readings that survive a restart, listed on the page.

### Add the database helper

New imports at the top:

```python
import sqlite3
from contextlib import contextmanager
```

Then, just after `app = FastAPI()`:

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
```

The `finally` block is the point: whatever happens inside, the connection gets
closed. A connection left open is a resource leak, and in a server that runs for
weeks it eventually becomes a crash. Writing it once here makes every use safe.

### Create the table

```python
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

> ### A trap you will hit in Stage 5
>
> `CREATE TABLE IF NOT EXISTS` will **not** change a table that already exists.
>
> In Stage 5 we add two columns. When you do, you must **delete `readings.db`**
> and restart, or you will get an error about a missing column and no
> explanation of why.

### Save each reading

Replace the body of `create_reading`:

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

    return {
        "id": new_id,
        "sensor": reading.sensor,
        "value": reading.value,
        "unit": reading.unit,
        "severity": severity,
    }
```

> ### Why the question marks?
>
> `VALUES (?, ?, ?)` with the values passed separately is a **parameterised
> query**. The database receives the command and the data as two different
> things.
>
> **Never build SQL by joining strings together.** That is how SQL injection
> attacks work: someone sends a "sensor name" that is actually a command, and
> your database runs it. The question marks make that impossible, and they cost
> nothing.

### Add an endpoint to read them back

```python
@app.get("/readings")
def list_readings(limit: int = 20):
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]
```

Note that `/readings` now has **two** endpoints: a POST that stores, and a GET
that lists. Same address, different methods, different code. That is normal and
deliberate.

### Update the page

Copy `stages/stage4/static/index.html`. It adds a table underneath, and this:

```javascript
// Fetch everything the server has stored and draw the table.
async function loadHistory() {
  const rows = await (await fetch("/readings")).json();
  ...
}
```

### See the result

Send three or four readings. They now appear in a table below.

| Time | Reading | Severity |
|---|---|---|
| 08:06:46 | co2 1450ppm | **critical** |
| 08:06:46 | spo2 97% | **normal** |
| 08:06:46 | body_temp 39.4C | **critical** |

### Now prove it is real

1. Stop the server — `Ctrl + C`
2. Start it again — `uvicorn main:app --reload`
3. Refresh the page

**The readings are still there.** And a new file called `readings.db` has
appeared in your folder. That file *is* the database.

> Do this comparison if you can: open Stage 3 and Stage 4 side by side, send
> readings to both, restart both, and refresh. Stage 3 is blank. Stage 4 is not.
> That is what a database is, in one move.

### New term

> **SQLite** — a complete database inside a single file. Nothing to install, no
> server to run, no password. For a prototype it is genuinely the right choice,
> and a great deal of production software uses it.

---

# Stage 5 — The AI explains

**Goal:** a written explanation alongside every verdict.

## First, a design decision

Before any code. This is the most useful idea in the workshop.

Look at `classify()`. It compares numbers. It is instant, free, correct every
time, and you can write a test for it.

**Do not give that job to an AI.**

Tested on the same eight readings, three runs each, asking only *"is this inside
the safe range?"*:

| Approach | Correct |
|---|---|
| Plain Python arithmetic | **100 %** |
| A small language model | 38 % |
| A larger language model | 83 % |

On a yes-or-no question, guessing scores about 50 %. The small model did worse
than guessing, because it has a habit of raising the alarm even when everything
is fine.

And the larger one classified **87 °C as "normal"** when the safe range was
20–60 °C — on two runs out of three.

> A false negative is the worst kind of error here. Saying "critical" when
> things are fine is annoying. Saying "normal" when the motor is overheating is
> the failure that matters.
>
> It is also **not repeatable**. The same question gave different answers. You
> cannot write a passing test for something that changes its mind.

### So we split the work

| | Your code decides | The AI explains |
|---|---|---|
| Produces | the severity | the sentence |
| Speed | instant | seconds |
| Correct? | always, by definition | usually |
| Testable? | yes | not really |
| If it fails | it cannot | the app still works |

**Comparing two numbers is not a job for a language model.** Writing a sentence
a tired engineer wants to read at 2am is — and that is something code genuinely
cannot do.

This is not "AI is bad". It is ordinary engineering judgement: know what each
component is good at, and do not route work to the wrong one.

## Now build it

### Create `.env`

A file called exactly `.env` in your project folder:

```
USE_MOCK=true
ANTHROPIC_API_KEY=
CLAUDE_MODEL=claude-haiku-4-5
```

> **Windows:** if you did not turn on file extensions in Part 0, Notepad will
> save this as `.env.txt` and your program will not find it. Check the filename.

### Create `.gitignore`

```
.env
*.db
__pycache__/
.venv/
```

> ### Create these two files now, before there is ever a real key to lose
>
> `.env` holds secrets. `.gitignore` is the list of files that must never be
> uploaded, and `.env` is the first line for a reason.
>
> Most people add `.gitignore` *after* they already have a key sitting in the
> folder. Doing it in this order is the habit worth building.

### Create `ai.py`

Everything to do with the AI lives in its own file — including the key.

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

### Three things worth noticing

**1. `anthropic.Anthropic()` takes no arguments.** It finds `ANTHROPIC_API_KEY`
in the environment by itself. **The key appears nowhere in your code.**

**2. `output_format=Advice` guarantees the reply.** The model cannot return a
paragraph, a refusal, or a differently named field. You get a validated object
back. Without this you would be writing code to find the useful part of some
prose, and that code breaks constantly.

**3. `USE_MOCK` means the whole application runs with no key at all.** You can
build, test, and even deploy before you have an account.

### Wire it into `main.py`

At the **very top**, above the other imports:

```python
from dotenv import load_dotenv
load_dotenv()          # read .env BEFORE anything else looks at the environment
```

> That looks wrong — imports are normally grouped together. It is deliberate.
> `load_dotenv()` must run before anything else reads the environment, and
> `import ai` reads it immediately.

With the other imports:

```python
import ai
```

Add two columns to the table in `init_db()`:

```python
                severity TEXT,
                reason   TEXT,
                action   TEXT
```

**Now delete `readings.db`.** (The trap from Stage 4.)

And update `create_reading`:

```python
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
```

Those two numbered comments are the design decision, written into the code.

### Update the page

Copy `stages/stage5/static/index.html`. It adds the explanation under the
verdict, and an Explanation column to the table.

### See the result

> **CRITICAL**
> your code checked: 36.1 ≤ 39.4 ≤ 37.2
>
> 39.4C against a safe range of 36.1-37.2C.
> *Set USE_MOCK=false to get a real AI answer.*

**With `USE_MOCK=true`, the application is complete and working with no AI
account at all.**

### Using a real key

If you have one, put it in `.env` and restart:

```
USE_MOCK=false
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Send another reading. The explanation is now written by the model.

**What it costs.** A request like this is roughly 500 tokens in, 150 out.

| Model | Per request | Requests per $5 |
|---|---|---|
| `claude-haiku-4-5` | $0.00125 | about 4,000 |
| `claude-opus-5` | $0.00625 | about 800 |

Two pieces of advice: set a spending limit on your account before you start, and
keep `USE_MOCK=true` while developing so you are not paying for every test run.

---

## What you have now

```
sensor-triage/
├─ main.py            your server: three endpoints
├─ ai.py              the AI call, and the only file that sees the key
├─ .env               your settings and secrets      (never uploaded)
├─ .gitignore         the list of things not to upload
├─ readings.db        the database                    (never uploaded)
└─ static/
   └─ index.html      the web page
```

A working full-stack application:

- **Frontend** — a page that sends readings and displays results
- **Backend** — three endpoints, with input validation
- **Data** — a database that survives restarts
- **An external service** — an AI API, with the key handled correctly

It runs on your laptop and nowhere else. **Part 4 puts it on the internet.**
