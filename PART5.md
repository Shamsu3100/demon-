# Part 5 — Where to go next

Your application is finished and deployed. This part is what to add when you
need it.

Each section is a pointer with enough code to start, not a full tutorial. Take
the ones your project actually needs and ignore the rest.

---

## 5.1 Connect a real device

This is the one most of you need, and it requires **no change to your server at
all.**

Your `/readings` endpoint accepts JSON. It does not know or care whether that
JSON came from a browser, a phone, a Python script, or a microcontroller.

### From an ESP32 or Arduino

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

const char* WIFI_SSID = "your-wifi-name";
const char* WIFI_PASS = "your-wifi-password";
const char* ENDPOINT  = "https://sensor-triage-xxxx.onrender.com/readings";

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(" connected");
}

void loop() {
  float reading = analogRead(34) * 0.1;      // <-- your sensor here

  WiFiClientSecure client;
  client.setInsecure();        // skip certificate checking (fine for a prototype)

  HTTPClient http;
  http.begin(client, ENDPOINT);
  http.addHeader("Content-Type", "application/json");

  String body = String("{\"sensor\":\"motor_temp\",\"value\":") + reading +
                ",\"unit\":\"C\",\"low\":20,\"high\":60}";

  int status = http.POST(body);
  Serial.printf("sent %.1f -> HTTP %d\n", reading, status);
  http.end();

  delay(60000);                              // once a minute
}
```

That is the whole integration. Your sensor readings now appear on a web page
anyone in the world can open.

### From a Python script or a Raspberry Pi

```python
import requests

requests.post(
    "https://sensor-triage-xxxx.onrender.com/readings",
    json={"sensor": "motor_temp", "value": 87,
          "unit": "C", "low": 20, "high": 60},
    timeout=10,
)
```

### Three practical notes

**`client.setInsecure()`** skips checking the server's HTTPS certificate. Fine
for a prototype on your own service; not what you would ship in a product.

**Watch the free tier's sleep.** If your device posts once an hour, the service
will be asleep every time and each post waits for a wake-up. Posting every few
minutes keeps it awake — which is itself a reason to consider a paid plan later.

**Send the range from the device or hardcode it in the server.** Right now the
device sends `low` and `high` every time. For a real deployment you would more
likely store safe ranges per sensor in the database, so the device only sends a
reading.

---

## 5.2 Where the other workshops plug in

Look at the ten sessions in this series. Every other one produces something that
lives **on a laptop or on a device**: a trained model, code on a microcontroller,
readings in a terminal, a PCB.

**Yours is the only one that ends with something anyone can open.** That makes
this application the natural place for the others to become visible.

| Workshop | What it gives you | Where it plugs in |
|---|---|---|
| **Predictive Analytics & AI Modelling** | a trained model | replace `classify()` with your model's prediction, or add an endpoint that runs it |
| **TinyML — Edge AI on Small Devices** | a model running on a chip | the device POSTs its prediction to `/readings` as the `value` |
| **Edge AI & Sensor Monitoring** | live sensor readings | exactly section 5.1 — no server changes |
| **Designing IoT Systems for Energy Saving** | power telemetry | same endpoint; the "reading" is watts |
| **Software Algorithms & Control** | control logic on a device | POST the state, display it, and read decisions back |
| **Engineering AI Prompting** | better prompts | the `SYSTEM` and `prompt` strings in `ai.py` |

### Replacing `classify()` with a trained model

If Workshop 3 gave you a model, the change is small:

```python
import joblib

model = joblib.load("model.pkl")


def classify(value: float, low: float, high: float) -> str:
    prediction = model.predict([[value, low, high]])[0]
    return prediction        # "normal" | "warning" | "critical"
```

Everything else — the endpoint, the database, the page, the deployment — is
unchanged. **That is what a clean boundary buys you.**

> One caution: add `scikit-learn` (or whatever you trained with) to
> `requirements.txt`, and commit the model file. Model files can be large;
> anything over about 100 MB will not fit in a normal git repository.

---

## 5.3 Keep your data when you redeploy

Free hosting wipes the disk on every deploy, so `readings.db` disappears.

**Fix:** use a managed database instead of a file.

1. In Render: **New → PostgreSQL**, choose the free plan
2. Copy the **Internal Database URL** it gives you
3. Add it as an environment variable, `DATABASE_URL`
4. Install `psycopg[binary]` and change how you connect

The concepts you learned do not change — a table, an `INSERT`, a `SELECT`. Only
the connection does.

> Render's free PostgreSQL expires after a period and then needs recreating.
> Check the current terms before relying on it for anything that matters.

---

## 5.4 Make it feel fast

Your `/readings` endpoint waits for the AI before replying. With a fast model
that is fine. With a slow one it is not — measured on the same question, five
times in a row: **4.7s, 4.9s, 7.5s, 17.1s, 26.4s.**

The problem is not that it is slow. It is that you **cannot predict** how slow,
so you cannot promise the user anything.

### The fix: answer first, explain afterwards

1. Compute the severity and save the row with `ai_status = "pending"`
2. **Return immediately** — the visitor has their answer in milliseconds
3. Do the AI call in a background task, and update the row when it finishes
4. The page polls until the explanation appears

FastAPI has this built in:

```python
from fastapi import BackgroundTasks


def fill_in_explanation(reading_id: int, ...):
    """Runs AFTER the response has already been sent."""
    advice = ai.explain(...)
    with db() as conn:
        conn.execute(
            "UPDATE readings SET reason=?, action=?, ai_status='done' WHERE id=?",
            (advice.reason, advice.action, reading_id),
        )


@app.post("/readings")
def create_reading(reading: Reading, background: BackgroundTasks):
    severity = classify(reading.value, reading.low, reading.high)
    # ... insert with ai_status='pending', get new_id ...

    background.add_task(fill_in_explanation, new_id, ...)   # queued, not awaited

    return {"id": new_id, "severity": severity, "ai_status": "pending"}
```

Measured on this application: the endpoint returned in **~30 ms** instead of
waiting 9 to 50 seconds. The slow part is still slow; it just stopped being the
visitor's problem.

> You have seen this pattern before. A messaging app shows your message
> instantly with one tick, then updates the delivery status a moment later. It
> did not wait for the network before showing you your own message.
>
> This applies far beyond AI. Any slow third party — payments, email, image
> processing — belongs behind this same structure.

---

## 5.5 Run the AI free, on your own machine

You can run a small language model locally with **[Ollama](https://ollama.com)**.
No account, no key, no cost, and it works with no internet connection.

```
ollama pull llama3.2:3b
```

Then add a branch to `explain()` in `ai.py` that posts to
`http://localhost:11434/api/chat`.

### The trap that will cost you a day

**`localhost` means "the computer running this code".**

On your laptop, that is your laptop, and Ollama is there. On your deployed
server, that is the server — and Ollama is not there. Your AI silently stops
working and the application keeps running as though nothing is wrong.

You cannot fix it by installing Ollama on the server either. A small model needs
around **4 GB** of memory; free hosting gives you about **512 MB**. It is not a
configuration problem you can solve; it does not fit.

### So decide your target before you build

| Your project runs... | Use |
|---|---|
| on a laptop at a table, possibly with no wifi | a local model — free, private, offline |
| at a public address people open remotely | a hosted API — needs a key, costs cents |

Both are valid. Choosing late is what costs you.

---

## 5.6 Control what you spend

Two limits, and you want both.

**1. On your provider account.** Set a hard monthly cap in their console before
you write any code. This is the one that actually protects you.

**2. In your application.** Refuse to send the request once you have spent
enough today:

```python
def check_budget():
    """Call BEFORE spending money. Raise rather than charge."""
    spent = todays_spend()          # you store this
    if spent >= MAX_USD_PER_DAY:
        raise RuntimeError(f"Daily cap reached (${spent:.4f})")
```

Then record the real cost afterwards, using the token counts the API reports
back rather than an estimate:

```python
usage = response.usage
cost = (usage.input_tokens / 1e6) * PRICE_IN \
     + (usage.output_tokens / 1e6) * PRICE_OUT
```

Normal use costs almost nothing. What costs money is a bug that retries forever
overnight, or a key someone else is using. The cap catches both.

---

## 5.7 Know when the AI has failed

A subtle one, and worth understanding.

Suppose you make `explain()` fall back to a plain sentence when the AI is
unreachable. That is good design — the application keeps working.

But it creates a new problem: **the failure becomes invisible.** The app looks
fine, the output looks plausible, and the AI has not run for three days.

Two rules:

**Log every fallback, with the reason.**

```python
except Exception as e:
    logging.warning("AI unavailable (%s), using fallback: %s", type(e).__name__, e)
    return fallback
```

**Never let the interface claim a model wrote something a model did not write.**
Store where the text came from — the model name, or `"rule"`, or
`"fallback:ConnectionError"` — and show it.

> This happened while building this workshop. The dashboard said "from the AI
> model" above text an `if` statement had written. It was only noticed because
> someone asked what the label meant.
>
> **Degrade gracefully, but log loudly.** Any fallback path in any system needs
> to be visible, or you will not find the bug.

---

## 5.8 Where to learn more

| Topic | Where |
|---|---|
| FastAPI | **fastapi.tiangolo.com** — genuinely excellent, start with the tutorial |
| Git | **git-scm.com/book** — free, thorough |
| HTTP and the web | **developer.mozilla.org** (MDN) — the reference everyone uses |
| Render | **render.com/docs** |
| Databases | the PostgreSQL tutorial, once SQLite stops being enough |

### The three things to learn next

1. **Authentication** — how to require a login. Right now anyone can post to
   your endpoint. FastAPI's security documentation covers this.
2. **Testing** — writing code that checks your code. `pytest` plus FastAPI's
   `TestClient`. Your `classify()` function is an ideal first test.
3. **Managed databases** — section 5.3, when data needs to survive.

---

## What you actually learned

The application is a vehicle. What transfers is underneath it:

- **A backend receives requests and decides what to send back.** Every web
  service works this way.
- **The frontend is public and the backend is not.** That single fact decides
  where secrets live.
- **Validate input at the edge**, because anyone can send anything.
- **Know what each component is good at.** Arithmetic to code, language to a
  language model.
- **Anything slow or external is allowed to fail** — but make the failure
  visible.
- **Pin your dependencies**, or your build breaks on a day you did not touch it.
- **Config belongs outside your code**, so the same program runs anywhere.

None of that is FastAPI, Render, or this application. It is how software gets
built, and the next thing you build will have the same shape.
