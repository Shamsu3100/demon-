# Part 4 — Put it on the internet

Your application works. It works on exactly one computer, and only while that
computer is awake with a terminal open.

This part moves it to a machine that never sleeps, at an address anyone can
open.

---

## 4.1 What "deploying" actually means

Three things have to happen.

| | |
|---|---|
| **1. Your code has to get there** | you cannot email a folder to a server. This is what GitHub is for |
| **2. The server has to know how to run it** | it starts empty: no Python packages, no start command |
| **3. It has to keep running** | if it crashes at 3am, something must restart it |

We solve them in that order: two small files, then GitHub, then Render.

Nothing about your application changes. `main.py`, `ai.py` and `index.html` are
finished. Everything in this part is **around** your code, not inside it.

---

## 4.2 The two files a server needs

### `requirements.txt` — what to install

Your laptop has FastAPI because you installed it. The server starts completely
empty. This file is the shopping list.

```
fastapi==0.141.1
uvicorn[standard]==0.34.0
pydantic==2.10.4
python-dotenv==1.0.1
anthropic==1.0.0
```

To see your own exact versions:

```
pip freeze
```

> ### Pin the versions
>
> Writing `fastapi` with no `==` version means the server installs whatever is
> newest **on the day it builds**. Your application then breaks weeks later
> without you touching a single line of code.
>
> This is not hypothetical. While preparing this workshop, installing an
> unrelated package upgraded a library underneath FastAPI and broke the
> application. `requirements.txt` had pinned FastAPI, but not the library
> beneath it.
>
> Pin everything. `pip freeze` gives you the exact list.

### `render.yaml` — how to run it

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
        value: "true"             # change to "false" once you have added a key

      # 'sync: false' means: this setting exists, but its value is typed
      # into the Render dashboard, never written in this file.
      # This file is uploaded to GitHub. A key must never be in it.
      - key: ANTHROPIC_API_KEY
        sync: false
```

Line by line:

| | |
|---|---|
| `type: web` | this service receives web requests |
| `runtime: python` | it is a Python project |
| `plan: free` | the free tier |
| `buildCommand` | runs **once**, when the code arrives |
| `startCommand` | runs to keep the application alive |
| `healthCheckPath` | the address Render calls to check you are alive |

**`/health` was worth writing in Stage 1 after all.** Render will call it every
few seconds, and restart your service if it stops answering.

### Three details worth understanding

**`--host 0.0.0.0`**

On your laptop, uvicorn listens only for requests from your own machine. On a
server that would make it unreachable. `0.0.0.0` means *accept requests from
anywhere*.

**`--port $PORT`**

The hosting platform chooses the port and tells your application through an
environment variable.

Hardcode `8000` here and you get a confusing failure: the logs look healthy, the
service says it started, and the address shows nothing — because the platform is
sending traffic to a door your app is not standing behind.

**`sync: false`**

This is the important one.

`render.yaml` gets **uploaded to GitHub**. A key written as a `value:` here is
published exactly as if you had pasted it into your source code.

`sync: false` says: *this setting exists, but its value is not in this file.* You
type the value into Render's dashboard afterwards, where it is private.

> **Any file that gets committed is a place a secret can hide.** `.env` is not
> the only one. Configuration files, CI workflow files, notebooks, Docker files.
> Build the habit of asking *"is this file uploaded?"* before typing a secret
> anywhere.

---

## 4.3 Git, in five minutes

You installed git in Part 0. Here is what it actually does.

### The four words you need

> **Repository** (**repo**) — one project's folder, with all of its history.
> Your `sensor-triage` folder becomes one.

> **Commit** — a saved checkpoint. It records exactly what every file looked
> like at that moment, with a message saying what changed.

> **Remote** — a copy of your repository somewhere else. Ours will live on
> GitHub.

> **Push** — send your commits to the remote.

### The mental model

```
   your folder  ──commit──▶  local history  ──push──▶  GitHub
```

Git records checkpoints on **your machine** first. Pushing copies them
somewhere else. That is why git works perfectly well offline, and why GitHub is
optional right up until you need another computer to see your code.

### Why we need it here

Render does not want a zip file. It connects to GitHub, reads your repository,
and rebuilds your application from it. Every time you push, it can redeploy
automatically.

---

## 4.4 Put your code on GitHub

### Create the repository on GitHub

1. Go to **<https://github.com/new>**
2. **Repository name** — `sensor-triage` is fine
3. Choose **Public** or **Private** — either works with Render
4. **Do not tick** "Add a README file", ".gitignore", or "Choose a licence"

> Those three tick-boxes create files on GitHub, which conflicts with the files
> you already have locally, and produces a confusing error on your first push.
> Start empty.

5. Click **Create repository**

GitHub now shows a page of setup commands. We use them below.

### Turn your folder into a repository

Back in your terminal, in your `sensor-triage` folder:

```
git init
```

```
git add .
```

`git add .` stages everything in the folder — except whatever `.gitignore`
excludes.

### Check what you are about to upload

**This is the most important command in the whole workshop.**

```
git status
```

Read the list carefully. You should see `main.py`, `ai.py`, `static/`,
`requirements.txt`, `render.yaml`, `.gitignore`.

> ### `.env` must NOT be in that list
>
> Nor should `readings.db`, `.venv`, or `__pycache__`.
>
> If `.env` appears, **stop**. Your `.gitignore` is missing or misspelled. Fix
> it, run `git add .` again, and check again.
>
> Three seconds here prevents the problem in the next section, which has no
> clean fix.

### Make your first commit

```
git commit -m "Sensor triage service"
```

The `-m` is the message. Write what changed, for the version of you that reads
it in three months.

### Connect it to GitHub and push

Replace the URL with your own — GitHub showed it on the page after you created
the repository:

```
git remote add origin https://github.com/YOUR-USERNAME/sensor-triage.git
```

```
git branch -M main
```

```
git push -u origin main
```

The first time, a window may open asking you to sign in to GitHub. Do so; your
computer remembers it afterwards.

Refresh your repository page. **Your code is on the internet** — though not yet
running anywhere.

---

## 4.5 Why "I deleted it" does not work

Run this demonstration, or at least read it carefully. It is the single most
expensive mistake in this workshop.

**What happens:**

1. You accidentally commit a file with your API key in it, and push
2. You notice, delete the key, commit again, and push
3. The file on GitHub now looks completely clean

**And yet anyone who clones your repository can run:**

```
git show <earlier-commit>:main.py
```

```python
client = anthropic.Anthropic(api_key="sk-ant-api03-REDACTED")
```

**The key is still there.**

Git's whole purpose is remembering every version. Deleting a line creates a
*new* commit; it does not remove the old one. The old version is still in the
history, and the history is what gets uploaded.

Rewriting history does not save you either. By the time you notice, the
repository has been cloned, cached, and scanned.

> ### The only real fix
>
> If a key has been pushed — even for one minute, even to a private repository —
> **treat it as stolen.**
>
> Go to the provider's website, delete that key, and create a new one. It takes
> thirty seconds and it is the only action that actually works.

Providers also scan public repositories automatically and disable keys they
find, often within minutes. Your application then dies with a `401` error at the
worst possible time.

**This is why `git status` before your first push is worth the three seconds.**

---

## 4.6 Deploy on Render

You created the account in Part 0. Now we use it.

### The steps

1. Go to **<https://dashboard.render.com>**

2. Click **New** (top right) → **Blueprint**

   > **Blueprint** is Render's word for "read the `render.yaml` file and set
   > everything up from it". The alternative is filling in a form by hand;
   > the file is better, because it is version-controlled and repeatable.

3. If asked, **connect your GitHub account** and give Render access — either to
   all repositories, or just to `sensor-triage`

4. Select **`sensor-triage`** from the list

5. Render reads your `render.yaml` and shows what it is about to create. It
   should show one web service on the free plan

6. Click **Apply** (or **Create**)

### Now wait

The first build takes **two to four minutes**. You will see a log scrolling past:

```
==> Cloning from https://github.com/...
==> Running build command 'pip install -r requirements.txt'
    Collecting fastapi==0.141.1
    ...
==> Build successful
==> Running 'uvicorn main:app --host 0.0.0.0 --port $PORT'
INFO:     Uvicorn running on http://0.0.0.0:10000
==> Your service is live
```

> **Errors and a blank page during this time are normal, not failure.** The
> service does not exist until the build finishes. Read the log rather than
> refreshing the address.

### See the result

At the top of the page is your address:

```
https://sensor-triage-xxxx.onrender.com
```

Open it. **Open it on your phone.** Send it to someone in another country.

Your application is on the internet.

### Check the pieces

| Address | Should show |
|---|---|
| `/` | the page you built |
| `/health` | `{"status":"ok"}` |
| `/docs` | the interactive API page |

`/docs` being live is worth noticing: anyone can now explore your API. That is
often what you want, and occasionally what you do not — real services put
authentication in front of it.

---

## 4.7 Adding your API key in production

Your deployed application is running with `USE_MOCK=true`, which is why it
needed no key.

If you have one:

1. In Render, open your service → **Environment**
2. Find **`ANTHROPIC_API_KEY`** — it exists with no value, because of
   `sync: false`
3. Paste your key in and **Save**
4. In your own `render.yaml`, change `USE_MOCK` to `"false"`
5. Commit and push

That fifth step is not optional, and here is why.

> ### The dashboard does not always win
>
> Changing `USE_MOCK` in Render's dashboard **will not work**. `render.yaml`
> gives it a `value:`, and the file is the source of truth.
>
> I lost fifteen minutes to this while preparing this workshop: changed the
> value in the dashboard, watched, and nothing happened.
>
> **The rule once you use a configuration file:**
> settings with a `value:` in the file → change the file and push.
> settings with `sync: false` → change them in the dashboard.

---

## 4.8 Updating your application

This is the part that makes deployment worth doing properly.

```
git add .
```

```
git commit -m "what you changed"
```

```
git push
```

That is it. Render notices the push and rebuilds automatically. A minute or two
later your change is live.

You now have a real development cycle: **edit locally → test locally → commit →
push → it is live.**

---

## 4.9 Things that will surprise you

### Your app falls asleep

Free services stop after about **15 minutes** with no visitors. The next person
to arrive waits **30 to 60 seconds** while it wakes up, staring at a blank tab.

Nothing is broken. It is how free tiers work.

**Before any demonstration, open your own link ten minutes early.** It costs
nothing and it means your visitor gets an awake server.

### Your stored readings disappear

Free plans give your service a **temporary disk**. Every deploy gives you a
fresh one, and `readings.db` is on it.

Your application still works perfectly. The history is just empty again.

If data must survive, that is the moment to add a managed database — Render
offers a free PostgreSQL instance. It is a change to how you connect, not to
your application's logic.

### The build failed

Open the **Logs** tab and read from the top. The first error is the real one.

| Log says | Usually means |
|---|---|
| `ERROR: Could not find a version...` | a typo or wrong version in `requirements.txt` |
| `ModuleNotFoundError` | a package you use is missing from `requirements.txt` |
| `No such file or directory: 'static'` | the `static` folder was not committed |
| service starts then stops | `startCommand` is wrong, or the port is hardcoded |
| `yaml: line N` | indentation in `render.yaml` — YAML is strict about spaces |

### It works locally but not deployed

The usual cause is something that exists on your machine and not on the server:

- a package installed but missing from `requirements.txt`
- a file that `.gitignore` excluded — check with `git status`
- a setting that is in your `.env` but not in Render's Environment tab
- anything pointing at `localhost`, which on a server means **the server**

---

## What you have now

```
   your laptop  ──push──▶  GitHub  ──reads──▶  Render  ──serves──▶  anyone
```

- A repository with your project's full history
- An application running on a machine that never sleeps
- A public address that works from any device, anywhere
- HTTPS, a health check, and automatic restarts, none of which you configured
- A one-command update cycle

**Part 5** covers where to take it next, and how the other workshops in this
series plug into what you have just built.
