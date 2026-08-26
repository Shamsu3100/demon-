# Part 1 — What these technologies actually are

No code in this part.

By the end of it you should be able to read a job advert, a tutorial, or a
hosting company's pricing page and know what the words mean — and choose where
to put your own project, with a reason.

---

## 1.1 What "full-stack" means

An application people reach over the internet has three parts.

| Part | What it is | Where it runs | Who can see it |
|---|---|---|---|
| **Frontend** | the page: buttons, text, layout | in the visitor's browser | **everyone** |
| **Backend** | your program: the logic | on a server | only you |
| **Data** | what is kept between visits | on a server | only you |

"Full-stack" means you build all three. That is what we are doing today.

### The line that matters most

**Everything the frontend receives has been handed to the visitor to keep.**

When someone opens your page, you are not showing it to them. You are sending
them a copy. The HTML, the styling, the JavaScript, and anything you left
inside it.

Prove it now: open any website, press `F12`, and look at the **Sources** or
**Network** panel. Every file that page sent is listed, and you can read all of
them.

There is no setting that prevents this. It is how browsers work.

That single fact decides where your API key is allowed to live — which is
section 1.8, and the reason the backend exists at all.

---

## 1.2 Request and response

Every action on the web is two steps.

```
   browser  ──────── request ────────▶  server
   browser  ◀─────── response ────────  server
```

- A **request** is a question sent over the internet.
- A **response** is the answer.

Opening a page is a request and a response. Pressing a button is a request and
a response. Loading an image, submitting a form, sending a message — all the
same shape, repeated very fast.

### The two kinds you will use

| | Meaning | Example |
|---|---|---|
| **GET** | *give me something* | opening a page |
| **POST** | *here is something* | submitting a form |

There are others (`PUT`, `DELETE`, `PATCH`), and they follow the same idea. You
need these two today.

### What a status code is

Every response carries a three-digit number saying how it went. You will see
these constantly:

| Code | Meaning |
|---|---|
| **200** | fine |
| **404** | there is nothing at that address |
| **422** | you sent something, but it was the wrong shape |
| **500** | your code crashed |

Learning to read these saves enormous time. A 404 and a 500 are completely
different problems: 404 means your address is wrong, 500 means your address was
right and the code behind it broke.

**Your job as a backend developer is to write the code that decides what goes
in the response.** Not the internet, not the browser. Just that.

---

## 1.3 What a server is

A computer that stays switched on, waiting for requests.

That is the whole idea. Not a special kind of machine — an ordinary computer
with a boring job and a permanent address.

For most of this workshop, **the server is your own laptop.** You will run one
in Part 3 and visit it in your own browser. It is a real server; it is just not
reachable by anyone else.

Deploying, in Part 4, means moving that same program onto a computer that never
sleeps and does have a public address.

### What a port is

You will type addresses like `127.0.0.1:8000`. The `:8000` is the **port**.

One computer can run many programs that all listen for requests. The port is
how it knows which one you want — like flat numbers in an apartment building,
where the address gets you to the building and the number gets you to the door.

- `127.0.0.1` (also written `localhost`) always means **this computer, right
  here**
- `:8000` means the program listening on port 8000

Two things to remember:

1. **Two programs cannot use the same port.** `Address already in use` means
   something else is already there — usually a server you forgot to stop.
2. **`localhost` is relative.** On your laptop it means your laptop. On a
   server it means the server. This causes a real and confusing bug, covered in
   Part 5.

---

## 1.4 What "the cloud" actually is

Someone else's computer, in a building somewhere, rented to you by the hour.

That is not a joke or a simplification. When you deploy to "the cloud", a
company with a warehouse full of machines gives you a slice of one, keeps it
powered and connected, and charges you for it. The word makes it sound
weightless; it is a building with air conditioning and a large electricity bill.

### What you are actually paying for

| | |
|---|---|
| **Uptime** | someone else keeps the power and network on |
| **An address** | a permanent, reachable location |
| **Maintenance** | security patches, failed disks, cooling |
| **Elasticity** | more capacity when you need it, less when you do not |

You could do all of this yourself with a computer at home. People do. You would
be responsible for power cuts, your home internet address changing, security
updates, and the machine dying at 3am.

For a student project, renting is obviously correct. Knowing *what* you are
renting is the point of the next section.

---

## 1.5 The four ways to host code

This is the section that transfers to every project you ever build. Hosting
comes in four shapes, and they differ in one thing: **how much you hand over.**

### 1. Static hosting

- **You give them:** finished files — HTML, CSS, images, JavaScript
- **They give you:** an address that serves those files, very fast
- **Examples:** GitHub Pages, Netlify, Cloudflare Pages, Vercel

Nothing runs on the server. It hands out files exactly as you uploaded them.

- Almost always free, and extremely fast
- **Cannot run Python.** Cannot use a database. Cannot hold a secret
- Anything it sends is public, by definition

Right for a portfolio, documentation, or a landing page. **Wrong for us**,
because we need Python to run and a key to stay hidden.

### 2. Platform hosting  ← *what we will use*

- **You give them:** your code, and a command to start it
- **They give you:** a machine that runs it, with an address and HTTPS
- **Examples:** Render, Railway, Heroku, Fly.io, PythonAnywhere, Google App Engine

You never touch the operating system. You do not install Python, configure a
web server, or set up certificates. You push code; it runs.

- Fastest path from code to a working address
- Usually has a free tier
- Less control — you get their machine, their versions, their limits
- Free tiers sleep when idle, and wake slowly

Right for prototypes, small applications, and almost every student project.

### 3. Server hosting

- **You give them:** nothing. You rent an empty computer
- **They give you:** a bare Linux machine and its address
- **Examples:** AWS EC2, DigitalOcean, Linode, Hetzner, Azure Virtual Machines

You install Python. You configure a web server. You set up HTTPS certificates,
a firewall, automatic restarts, and security updates. Forever.

- Complete control; run anything
- Cheapest at scale
- **You are now a system administrator**, whether or not you wanted to be
- No free tier that lasts; typically a few dollars a month

Right when you have outgrown a platform, or need something unusual installed.
Wrong as a first deployment — you will spend the workshop on Linux
configuration rather than on your application.

### 4. Serverless

- **You give them:** a single function
- **They give you:** that function run on demand, as often as needed
- **Examples:** AWS Lambda, Google Cloud Functions, Azure Functions, Cloudflare
Workers, Vercel Functions

There is no machine you think about. Your function sits dormant, and each
request wakes a copy of it.

- Costs nothing when nobody is using it
- Scales to enormous traffic without you doing anything
- **Cold starts:** the first call after a quiet period is slow
- Time limits per call — long jobs do not fit
- Nothing is remembered between calls; a local file is gone next time
- Awkward for a whole application; natural for one task

Right for a webhook, a scheduled job, or one endpoint called occasionally.
Wrong for a first full-stack app, where the pieces need to sit together.

### Side by side

| | Static | **Platform** | Server | Serverless |
|---|---|---|---|---|
| You provide | files | **code** | nothing | a function |
| Runs your Python | no | **yes** | yes | yes |
| You manage the OS | no | **no** | **yes** | no |
| Can hold a secret | no | **yes** | yes | yes |
| Free tier | yes | **yes** | rarely | yes, generous |
| Sleeps when idle | no | **yes (free tier)** | no | yes |
| Setup effort | minutes | **minutes** | hours | moderate |
| Control | none | **some** | total | little |

### So why Render?

Platform hosting, because we need Python to run and a secret to stay hidden —
which rules out static — and we do not want to spend the session administering
Linux, which rules out a bare server. Serverless would work for one endpoint but
fights us on a full application with a database.

Among platforms, Render because:

- The free tier needs **no credit card** — this matters for a student cohort
- One configuration file describes the whole service
- It reads directly from GitHub

**Railway, Fly.io and PythonAnywhere would all work.** Nothing in this workshop
is Render-specific except the shape of one configuration file. If you already
use another, use it.

### When you would outgrow it

- Real, continuous traffic — the free tier's sleeping becomes unacceptable
- You need more memory or CPU than the free plan allows
- You need files to survive a redeploy (free plans wipe the disk)
- You need something unusual installed at system level
- At large scale, renting a plain server becomes cheaper

Moving is not dramatic. Your code does not change. The configuration around it
does.

---

## 1.6 Things you will see but not touch today

### HTTPS and the padlock

`https` rather than `http` means the traffic between browser and server is
encrypted. Someone watching the network sees that you contacted the site, but
not what was sent.

Every hosting provider in this workshop provides it automatically and free. On
a bare server you would set it up yourself.

**Anything handling a password, a payment, or personal data must use HTTPS.**
Browsers now mark plain `http` pages as insecure.

### Domain names

`sensor-triage.onrender.com` is a **domain name**. Computers actually find each
other by number (an IP address); domain names exist because people cannot
remember numbers. The lookup system that translates one to the other is called
**DNS**.

Your free address is a name underneath your provider's own domain. A domain of
your own costs roughly ten to fifteen dollars a year, and you point it at your
application by changing one DNS record. Not needed today.

### Containers, and Docker

A **container** packages your code together with everything it needs to run:
the right Python version, the right libraries, the right system tools.

The problem it solves is old and familiar: *"it works on my machine."* It works
on yours because your machine has things the server does not. A container
carries those things with it, so the code runs identically everywhere.

**Docker** is the tool most people use to build them. Container hosting — Google
Cloud Run, AWS ECS, Kubernetes — sits between platform and server hosting: more
control than a platform, less administration than a bare machine.

We do not need it today. Our platform builds the equivalent for us from
`requirements.txt`. Learn it when you need to guarantee that something runs the
same way in two places.

### Why the server needs `requirements.txt`

Your laptop has FastAPI installed because you installed it. The server starts
completely empty.

`requirements.txt` is a list of what to install. The server reads it, downloads
each package, and only then starts your program. Without it, your code fails on
its first `import`.

---

## 1.7 What an API is

A way for your program to ask another program a question over the internet, and
get an answer back.

That is all. No more mysterious than a request and a response — because that is
exactly what it is.

You have used APIs already without the word:

- A weather app asking a weather service for today's forecast
- A payment button asking a bank whether a card is valid
- A map showing live traffic
- Signing in to a site "with Google"

### Why we need one for AI

The large AI models need far more memory and processing power than a laptop
has. So your program does not run the model. It sends the question to a company
that can, and reads the answer.

```
   your program  ──── question ────▶  a very large computer
   your program  ◀──── answer ─────   running the model
```

You send text. You get text back. Your own machine does almost no work.

> **Note:** smaller AI models *can* run on a laptop — Part 5 covers this. But
> they need several gigabytes of memory, which is more than free hosting
> provides. That trade-off is a real decision, and Part 5 explains it.

### Two APIs, two directions

Worth being clear about, because the word gets used for both:

- Today you **use** an API — you call an AI company's service
- Today you also **build** one — your `/readings` endpoint is an API, and in
  Part 5 a microcontroller calls it exactly as you called the AI company's

Same idea, opposite ends.

---

## 1.8 What an API key is

A long secret string that identifies your account with a service.

```
sk-ant-api03-x8Kq2vN...
```

### Why it deserves care

An API key behaves like **a bank card with no PIN**.

There is no second step, no confirmation, no approval email. Whoever holds it
can use your account and spend your money. Possession is the entire security
model.

So:

- It must never appear in your code
- It must never be sent to a browser
- It must never be uploaded to GitHub
- It must never be in a screenshot, a video, or a group chat

### Where it goes instead

In a small file called `.env`, which stays on your computer and is never
uploaded. Your program reads it at the moment it runs.

> **This is what an *environment variable* is:** a setting supplied to a program
> when it starts, rather than written inside it. The same code then runs
> unchanged on your laptop and on the server — each reads its own settings.

And now the two halves of Part 1 meet:

**The frontend is public (1.1). An API key must stay secret (1.8). Therefore
the key cannot live in the frontend.**

It lives on your backend, which the visitor never sees. **That is what the
backend is for.** If you only had a static page, you would have nowhere safe to
put it.

```
   browser  ──▶  your server  ──▶  AI company
                (holds the key)
```

The browser sends only the data. Your server adds the key and passes the
question on. The key never travels to the visitor, so it can never be taken.

---

## 1.9 Where data lives

### A file

We will use **SQLite** — a complete database inside a single file. Nothing to
install, no server, no password. Your program opens the file and uses it.

For a prototype it is genuinely the right choice, and plenty of production
software uses it.

### A managed database

**Postgres** and **MySQL** are databases that run as their own service, on their
own machine, that many programs can use at once. Hosting providers rent them by
the month, and some offer a small free one.

### Which, and when

| | A file (SQLite) | A managed database |
|---|---|---|
| Setup | none | an account and a connection string |
| Cost | free | free tier, then monthly |
| Many programs at once | poor | designed for it |
| Survives a redeploy | **no, on free hosting** | yes |

That last row is the one that matters, and it surprises people.

**Free hosting wipes the disk every time you deploy.** Your database file is
part of that disk, so everything stored in it disappears when you push an
update. The application still works; the history is empty.

For today that is fine — we are learning the shape, not running a business. If
your project needs data to survive, that is the moment to add a managed
database, and it is a small change.

---

## 1.10 The wider landscape

Everything in this workshop is one choice out of several at each layer. None of
those choices is the only correct one, and knowing the alternatives is what lets
you make your own decision on the next project.

For each layer: what exists, and why we picked what we picked.

### The backend framework

What runs your server code.

| | Language | Notes |
|---|---|---|
| **FastAPI** | Python | what we use. Automatic validation and an automatic test page |
| Flask | Python | older and simpler. No automatic validation or docs |
| Django | Python | batteries included: admin panel, user accounts, database layer. Heavier |
| Express | JavaScript | the default in the Node world |
| Spring Boot | Java | the enterprise standard |
| Gin, net/http | Go | compiled and very fast |
| Rails, Laravel | Ruby, PHP | mature and highly opinionated |

**Why FastAPI:** you already write Python for AI and engineering work, so there
is no second language to learn. The automatic validation and the free `/docs`
page do real work for you, and neither Flask nor Express gives you those without
extra libraries.

### The frontend

What draws the page.

| | Notes |
|---|---|
| **Plain HTML and JavaScript** | what we use. No build step, nothing to install, works everywhere |
| React, Vue, Svelte | component frameworks for large interfaces. Require a build step |
| Streamlit, Gradio | Python only, no HTML at all. Extremely fast for a dashboard |
| Flutter, React Native | mobile applications |
| Native iOS / Android | full platform access |

**Why plain HTML:** the subject of this workshop is deployment, not interface
design. A build step is one more thing that can break in front of an audience,
and React would teach you React rather than teach you deployment.

> **The important point is underneath this table.** Every option above talks to
> the same backend, in the same way. Your `/readings` endpoint does not know or
> care whether the request came from plain JavaScript, a React application, a
> Flutter phone app, or a microcontroller.
>
> **Build the backend once, and every kind of client can use it.** That is why
> the split between frontend and backend exists at all.

### Streamlit and Gradio, specifically

Worth calling out, because for some projects they are genuinely the better
choice.

Both let you build a web interface in pure Python, with no HTML. A dashboard
that would take you an hour here takes about fifteen lines there.

**But neither one can receive a POST from a device.** They have no route
handlers. If your project has a microcontroller sending readings, you need a
real backend. If it is software only and you just need a face on it, Streamlit
will save you hours.

### The database

| | Type | Notes |
|---|---|---|
| **SQLite** | relational | what we use. A whole database in one file |
| PostgreSQL | relational | the general-purpose default for real applications |
| MySQL / MariaDB | relational | similar, extremely widely deployed |
| MongoDB | document | stores JSON-shaped records; flexible shape |
| Redis | key-value | in-memory and very fast; used for caching and queues |

Three broad categories, and the difference matters more than the brand:

- **Relational** — data in tables with fixed columns, queried with SQL. Right
  when your data has a consistent shape, which most sensor data does.
- **Document** — records that are JSON objects and need not all match. Right
  when the shape varies or changes often.
- **Key-value** — a very fast lookup by name. Usually a cache in front of
  something else, not your main storage.

**Why SQLite:** no installation, no configuration, no account. When it stops
being enough, PostgreSQL is the usual next step, and the SQL you learned still
applies.

### The AI provider

| | Notes |
|---|---|
| **Anthropic (Claude)** | what we use |
| OpenAI | similar shape and pricing model |
| Google (Gemini) | similar; a free tier is often available |
| Mistral, Cohere | smaller providers, competitive pricing |
| Ollama, vLLM | run open models on your own machine or server |
| Hugging Face | thousands of open models, hosted or downloaded |
| AWS Bedrock, Azure AI, Vertex AI | the same models, billed through a cloud provider |

**They nearly all follow the same shape:** send text plus a key, get text back.
The library differs, the endpoint differs, the parameter names differ slightly.
The idea does not.

That is exactly why our AI call lives alone in `ai.py`. Changing provider means
editing one file, and nothing else in the application notices.

### Automation, once your project is real

Not needed today, but you will meet these:

| | What it does |
|---|---|
| **Docker** | packages your code with everything it needs, so it runs identically anywhere |
| **GitHub Actions** | runs tasks automatically on every push: tests, checks, deployment |
| **pytest** | writes tests that check your code still works after a change |
| **Sentry, uptime monitors** | tell you your application broke before your users do |

### How to choose, on your next project

Four questions, in this order:

1. **Does anything need to send data to it?** If yes, you need a real backend.
   That rules out static hosting, Streamlit and Gradio.
2. **Do you have a secret to protect?** If yes, you need a backend. Same
   conclusion.
3. **What language do you already write?** Use it. Learning a framework is
   quick; learning a language while learning deployment is not.
4. **How long does it need to live?** A demonstration, a term project, and a
   product have very different answers, and it is fine to choose the cheap
   option for the first two.

**Almost every "which technology should I use" question is answered by one of
those four.**

---

## 1.11 What we are building

A **sensor triage service**.

Something sends a reading. Your code decides whether it is safe. An AI writes a
short explanation. The result is stored and displayed.

### Why this one

Because it is the shape every Project Nexus track shares: **a number, and a
range it should stay inside.**

| Track | Reading | Safe range |
|---|---|---|
| Healthcare | body temperature 39.4 °C | 36.1 – 37.2 °C |
| Healthcare | blood oxygen 88 % | 95 – 100 % |
| Sustainable Solutions | indoor CO₂ 1450 ppm | 400 – 1000 ppm |
| Sustainable Solutions | power draw 4800 W | 0 – 3500 W |
| Global Impact | soil moisture 8 % | 30 – 70 % |
| Global Impact | motor temperature 87 °C | 20 – 60 °C |

Same code for all of them. Only the numbers change.

When several different problems share one shape, you write one program instead
of several. Noticing that shape is a large part of software design.

### And where it fits in this series

Every other workshop in this series produces something that lives on a laptop or
on a device: a trained model, a program on a microcontroller, sensor readings in
a terminal.

**This is the session that puts those things somewhere other people can see
them.** The endpoint you build today accepts a reading from a browser — and it
accepts exactly the same reading from an ESP32, with no change to your code.

---

## Before you continue

You should now be able to answer these. If any is unclear, that section is
worth re-reading before Part 2.

1. Why can a static host not keep an API key safe?
2. What is the difference between platform hosting and server hosting?
3. What does `:8000` mean in `127.0.0.1:8000`?
4. Why does the server need `requirements.txt` when your laptop does not?
5. Why must the API key live on the backend rather than in the page?
6. What happens to your SQLite file when you redeploy on free hosting?
7. Why can Streamlit not receive a reading from an ESP32?
8. Name one reason you would choose PostgreSQL over SQLite.

---

**Part 2** is the fast path: a model out of a notebook and onto the internet in
twenty minutes. **Part 3** then builds the full application.
