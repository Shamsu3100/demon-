\newpage

# Appendix A — Glossary

Terms in the order you are likely to meet them.

**Terminal** — a window where you type commands instead of clicking.

**Virtual environment** (`.venv`) — a private copy of Python for one project, so
its packages do not affect anything else on your machine.

**Server** — a computer that stays switched on, waiting for requests. Nothing
more special than that.

**Request / Response** — a question sent over the internet, and the answer. Every
action on the web is this pair.

**GET / POST** — GET asks for something; POST sends something.

**Status code** — the number in a response saying how it went. 200 fine, 404
nothing at that address, 422 wrong shape, 500 your code crashed.

**Endpoint** — one address your server answers, and the code behind it.

**Port** — the number after the colon in `127.0.0.1:8000`. One computer runs many
programs; the port says which one you want.

**localhost / 127.0.0.1** — "this computer, right here". What "this computer"
means depends on where the code is running.

**Frontend** — the page in the visitor's browser. Public: anyone can read all of
it.

**Backend** — your program, running on a server. Private.

**Full-stack** — building the frontend, the backend, and the data storage.

**JSON** — the text format programs use to exchange data. Looks like a Python
dictionary.

**API** — a way for your program to ask another program a question over the
internet and get an answer.

**API key** — a secret string identifying your account with a service. Behaves
like a bank card with no PIN.

**Environment variable** — a setting supplied to a program when it runs, rather
than written inside it. Where secrets belong.

**SQLite** — a complete database inside a single file. Nothing to install.

**Parameterised query** — passing SQL and its values separately, using `?`. What
prevents SQL injection.

**The cloud** — someone else's computer, in a building somewhere, rented to you.

**Static hosting** — a host that serves finished files and runs no code of yours.

**Platform hosting** — you give them code and a start command; they run it. What
we use.

**Server hosting** — you rent a bare machine and administer it yourself.

**Serverless** — you give them one function; it runs on demand and costs nothing
when idle.

**Container / Docker** — packaging code together with everything it needs, so it
runs identically everywhere.

**HTTPS** — encrypted traffic between browser and server. The padlock.

**DNS** — the system that turns a name like `example.com` into a number.

**Git** — the program that records versions of your code, on your machine.

**GitHub** — a website that stores copies of git repositories online.

**Repository (repo)** — one project's folder, with all of its history.

**Commit** — a saved checkpoint in that history.

**Remote / Push** — a copy of your repository elsewhere, and sending your commits
to it.

**Deploy** — moving your application onto a server that stays on, at a public
address.

**Cold start** — the delay when a sleeping free service has to wake up.

**Pinning** — writing exact version numbers in `requirements.txt`, so future
builds install the same thing.

\newpage

# Appendix B — Command reference

## Terminal basics

| Command | What it does |
|---|---|
| `cd foldername` | go into a folder |
| `cd ..` | go up one folder |
| `dir` | list this folder's contents (macOS/Linux: `ls`) |
| `cls` | clear the screen (macOS/Linux: `clear`) |
| `Ctrl + C` | stop whatever is running |
| `Tab` | complete a name you have started typing |

## Python and the project

| Command | What it does |
|---|---|
| `python --version` | check Python is installed |
| `python -m venv .venv` | create the virtual environment |
| `.venv\Scripts\activate` | turn it on (Windows) |
| `source .venv/bin/activate` | turn it on (macOS/Linux) |
| `pip install <package>` | install a package |
| `pip freeze` | list exact installed versions |
| `uvicorn main:app --reload` | run the server |

## Git

| Command | What it does |
|---|---|
| `git init` | start tracking this folder |
| `git add .` | stage all changes |
| `git status` | **check what you are about to upload** |
| `git commit -m "message"` | save a checkpoint |
| `git remote add origin <url>` | connect to GitHub |
| `git push` | send commits to GitHub |
| `git log --oneline` | list your checkpoints |

## Useful addresses while developing

| Address | What it shows |
|---|---|
| `127.0.0.1:8000` | your web page |
| `127.0.0.1:8000/health` | the health check |
| `127.0.0.1:8000/docs` | the interactive API page |
| `127.0.0.1:8000/readings` | the stored readings, as JSON |

\newpage

# Appendix C — Troubleshooting

## Setup

| What you see | What it means | Fix |
|---|---|---|
| `python is not recognized` | the PATH box was missed on install | reinstall Python, tick **Add python.exe to PATH** |
| `git is not recognized` | terminal opened before installing | close it, open a new one |
| `running scripts is disabled` | Windows blocks scripts by default | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `cd` seems to do nothing | wrong drive, in Command Prompt | type `E:` on its own first |
| `The system cannot find the path` | a space in the path | wrap it in quotes: `cd "My Folder"` |
| macOS: `python: command not found` | macOS uses `python3` | use `python3` and `pip3` |

## Building

| What you see | What it means | Fix |
|---|---|---|
| `ModuleNotFoundError` | package missing, or venv not active | activate the venv, then `pip install` |
| `Address already in use` | an old server is still running | stop it, or `--reload --port 8001` |
| `/health` returns your HTML page | `app.mount("/")` is above your endpoints | move it to the last line of the file |
| `no such column: reason` | the table was made before you added columns | delete `readings.db` and restart |
| Your `.env` is called `.env.txt` | Windows hides file extensions | turn extensions on, rename it |
| `422 Unprocessable Entity` | your JSON does not match the `Reading` class | check field names and types |
| The page loads but Send does nothing | look at the browser console (`F12`) | the error is usually named there |

## Deploying

| What you see | What it means | Fix |
|---|---|---|
| Build fails: `Could not find a version` | wrong version in `requirements.txt` | check against `pip freeze` |
| Build fails: `yaml: line N` | indentation in `render.yaml` | YAML is strict; use spaces, not tabs |
| Service starts then stops | port hardcoded, or wrong start command | use `--port $PORT` |
| Address shows nothing, logs look fine | not listening on `0.0.0.0` | add `--host 0.0.0.0` |
| First visit takes 30-60 seconds | free service was asleep | normal; open your link before a demo |
| Stored readings gone after deploying | free plans wipe the disk | use a managed database if it matters |
| Works locally, not deployed | something exists on your machine only | check `requirements.txt`, `git status`, and environment settings |

## Reading an error

Three habits worth more than any table above:

1. **Read the first error, not the last.** Later errors are usually consequences.
2. **Read the whole message.** It almost always names the file, the line, and the
   problem.
3. **Check where you are** before assuming the code is wrong. Most "it does not
   work" moments are "I am in the wrong folder" or "the virtual environment is
   not on".

\newpage

# Appendix D — Checklist

Print this, or keep it open.

## Before you start

- [ ] `python --version` shows 3.10 or higher
- [ ] `git --version` works
- [ ] VS Code installed
- [ ] File name extensions visible (Windows)
- [ ] Logged in at github.com
- [ ] Logged in at render.com

## While building

- [ ] Virtual environment activated — you can see `(.venv)`
- [ ] `uvicorn main:app --reload` running, left running
- [ ] `app.mount("/")` is the **last** line of `main.py`
- [ ] `.gitignore` created **before** `.env`
- [ ] `readings.db` deleted after adding table columns

## Before you push

- [ ] `git status` run, and read
- [ ] `.env` is **not** in the list
- [ ] `readings.db`, `.venv`, `__pycache__` are **not** in the list
- [ ] No key written in `render.yaml`

## After deploying

- [ ] `/health` returns `{"status":"ok"}`
- [ ] `/` shows your page
- [ ] `/docs` loads
- [ ] Opened it on a phone, on mobile data, not on your own wifi

\newpage

# Colophon

Written for **Project Nexus 2026 — AI Innovation Challenge**, organised by the
IEEE Multimedia University Student Branch, with co-organisers E3S2 UTP,
IEEE PES MMU SBC, EWB MMU, and IEM MMU.

Every command and every line of code in this guide was executed and verified
before publication. The measured figures quoted in Part 3 and Part 5 — model
accuracy, response times, concurrency behaviour — were produced by running the
tests described, not taken from other sources.

The companion repository contains all six stage folders, each a complete working
application.
