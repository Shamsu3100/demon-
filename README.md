# Full-Stack App Deployment with AI APIs & Cloud

Workshop material for **Project Nexus 2026 — AI Innovation Challenge**
IEEE Multimedia University Student Branch · Workshop 4 of 10 · 31 August 2026

Build a web application from an empty folder, connect an AI API, and deploy it
to the public internet.

## Start here

**[GUIDE.md](GUIDE.md)** — the complete step-by-step guide. Every command, every
line of code, and a troubleshooting table.

## What you need

- Python 3.10 or newer
- A code editor
- A GitHub account (only for the final stage)

You do **not** need an AI account, an API key, or a credit card. The application
runs fully with `USE_MOCK=true`.

## Two paths

**Fast path** — `fastpath/` — a trained model online in about 20 minutes, with no
HTML and no server code. Notebook, model, Gradio app, deployed to Hugging Face
Spaces.

**Full path** — `stages/` — a complete application a device can send readings
to, deployed to Render.

Part 2 of the guide ends with a table showing which one your project needs.

## The full path, stage by stage

| | | |
|---|---|---|
| 1 | A server that answers | `stages/stage1` |
| 2 | An endpoint that accepts data | `stages/stage2` |
| 3 | Store the readings | `stages/stage3` |
| 4 | Connect the AI API | `stages/stage4` |
| 5 | The web page | `stages/stage5` |
| 6 | Deploy to the cloud | `stages/stage6` |

Work through the guide in **one folder of your own**, building it up stage by
stage. The folders above are complete working copies — if you fall behind, copy
the one you need and carry on.

## Running any stage directly

```bash
cd stages/stage6
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install "fastapi[standard]" uvicorn python-dotenv anthropic
cp .env.example .env
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000> for the app, or
<http://127.0.0.1:8000/docs> for the interactive API page.

## A note on secrets

`.env` holds your API key and is listed in `.gitignore`. It must never be
uploaded. Run `git status` before your first push and confirm `.env` is not
listed.

If a key is ever pushed, deleting it later does not remove it — git keeps every
past version. Delete that key at the provider and create a new one.
