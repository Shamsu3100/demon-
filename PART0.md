# Part 0 — Setting up your computer

**Nothing in this part is about our project.** It installs the four tools every
developer uses, and creates the two free accounts we need at the end.

If you already have Python, VS Code and Git working, skip to the checklist at
the end and confirm all four commands run.

Allow about 45 minutes the first time. You only ever do this once.

> Instructions are written for **Windows**, because most laptops in the room
> are Windows. Where macOS or Linux differs, it is marked like this:
> **macOS / Linux:** …

---

## 0.1 The terminal

### What it is

A window where you type commands instead of clicking. Every tool we use today
is driven from it.

It feels unfamiliar for about twenty minutes, then it stops being frightening.
You are not going to break anything: the commands in this guide only create
files and start programs.

### Opening it

**Windows** — any of these work:

1. Press the **Windows key**, type `powershell`, press **Enter**.
2. Or: right-click the **Start** button → **Terminal** or **Windows PowerShell**.
3. Or, best while working: open your project folder in File Explorer, click the
   address bar, type `powershell`, press **Enter**. This opens a terminal
   already in that folder.

**macOS:** press `Cmd + Space`, type `terminal`, press **Enter**.

You will see a line ending in `>` (Windows) or `$` (macOS). That is the prompt.
It is waiting for you.

### The five commands you actually need

| Command | What it does |
|---|---|
| `cd foldername` | go **into** a folder |
| `cd ..` | go **back up** one folder |
| `dir` | list what is in this folder (**macOS / Linux:** `ls`) |
| `cls` | clear the screen (**macOS / Linux:** `clear`) |
| `Ctrl + C` | stop whatever is running |

Two habits worth building now:

- **Press `Tab` to complete a name.** Type `cd sen` then `Tab` and Windows
  finishes `sensor-triage` for you. Fewer typos, much faster.
- **Look at the prompt before you run anything.** It shows which folder you are
  in. Most "it doesn't work" moments are really "I am in the wrong folder".

### Two Windows traps

**Paths with spaces need quotes.**

```
cd "E:\Nexus Training\workshop"
```

Without the quotes, Windows reads `E:\Nexus` and `Training\workshop` as two
separate things and fails.

**`cd` will not change drive letters in Command Prompt.** If your prompt says
`C:\>` and your work is on `E:`, type the drive letter on its own first:

```
E:
cd "E:\Nexus Training\workshop"
```

PowerShell does not have this problem. Command Prompt does. If a `cd` seems to
do nothing at all, this is usually why.

---

## 0.2 Show file extensions (Windows — do this first)

Windows hides the end of filenames by default. That single setting causes a
problem later in this workshop, so fix it now.

Later you will create a file called exactly `.env`. With extensions hidden,
Notepad silently saves it as `.env.txt`, your program cannot find it, and
nothing on screen tells you why.

1. Open **File Explorer**
2. Click the **View** menu
3. Turn on **File name extensions**

*(Windows 10: View tab → tick "File name extensions". Windows 11: View → Show →
File name extensions.)*

You should now see `main.py` rather than `main`. Two clicks, and it saves an
hour of confusion.

---

## 0.3 Python

### What it is

The language we write in. Your computer probably does not have it, and the one
that ships with macOS is too old to use.

### Installing it

1. Go to **<https://www.python.org/downloads/>**
2. Click the big yellow **Download Python 3.x** button
3. Run the file you downloaded

**On the first installer screen, before clicking anything:**

> ### ☑ Tick **"Add python.exe to PATH"**
>
> It is a small checkbox near the bottom and it is **off** by default.
>
> If you miss it, your terminal will say `python is not recognized` and you
> will have to reinstall. This is the single most common setup failure.

Then click **Install Now** and wait.

**macOS:** the installer has no PATH checkbox; it handles this itself.

**Linux:** `sudo apt install python3 python3-venv python3-pip`

### Checking it worked

**Close your terminal and open a new one** — this matters, because an already
open terminal does not know about newly installed programs.

```
python --version
```

You should see something like:

```
Python 3.13.7
```

Any version **3.10 or higher** is fine.

**If it says `python is not recognized`:** the PATH checkbox was missed. Run the
installer again, choose **Modify**, and make sure PATH is ticked. Or try `py --version`,
which sometimes works when `python` does not.

**macOS / Linux:** use `python3 --version`. On those systems, plain `python`
often means an old version 2, which will not work.

---

## 0.4 VS Code

### What it is

The editor we write code in. You could use Notepad, but VS Code colours your
code, points out mistakes as you type, and has a terminal built in.

It is free, from Microsoft, and it is what most professionals use.

### Installing it

1. Go to **<https://code.visualstudio.com>**
2. Click **Download**, run the installer, accept the defaults
3. On the "Select Additional Tasks" screen, tick
   **"Add 'Open with Code' action to directory context menu"** — it lets you
   right-click any folder and open it straight in the editor

### Two things to know

**Always open a *folder*, not a file.** `File → Open Folder`. VS Code shows
everything in that folder down the left side, and its built-in terminal starts
in the right place. Opening a single file gives you none of that.

**The built-in terminal:** `View → Terminal`, or `Ctrl + ~` (the key above
Tab). This is where you will type most commands, and it already knows which
folder you are in.

### The Python extension

The first time you open a `.py` file, VS Code offers to install the Python
extension. **Accept.** It adds error highlighting and autocomplete.

---

## 0.5 Git

### What it is — before you install it

Git records versions of your code. Every time you save a checkpoint (a
**commit**), it remembers exactly what every file looked like at that moment.

Two reasons we need it:

1. **You can go back.** If you break something on Thursday, you can return to
   Tuesday's working version.
2. **It is how code reaches a server.** Our hosting provider does not want a zip
   file. It collects your code from GitHub, and GitHub speaks git.

> **Git and GitHub are different things.**
> **Git** is the program on your computer that records versions.
> **GitHub** is a website that stores copies of those versions online.
> Git works perfectly well with no GitHub account. GitHub is where you put it so
> other computers can reach it.

### Installing it

1. Go to **<https://git-scm.com/downloads>** and click **Windows**
2. Run the installer

The installer asks a lot of questions. **Accept every default.** They are
sensible, and none of them matter for this workshop.

**macOS:** type `git --version` in Terminal — macOS offers to install it.

**Linux:** `sudo apt install git`

### Checking it worked

Open a **new** terminal:

```
git --version
```

```
git version 2.54.0.windows.1
```

Any version is fine.

### Tell git who you are (one time, ever)

Git labels every checkpoint with a name and an email. Set them once:

```
git config --global user.name "Your Name"
```

```
git config --global user.email "you@example.com"
```

Use the same email you will use for GitHub in the next section.

---

## 0.6 A GitHub account

### What it is

A website that stores your code online, for free. It is where almost all open
source software lives, and it is how our hosting provider will collect our
project.

Your account is also a public portfolio. Employers look at it.

### Creating one

1. Go to **<https://github.com/signup>**
2. Enter your **email address** — use one you can open right now
3. Choose a **password**
4. Choose a **username**

> **Choose the username carefully.** It becomes part of every web address you
> create: `github.com/your-username/your-project`. It is public and hard to
> change later.
>
> Something close to your real name is a good choice. Avoid anything you would
> not want on a CV.

5. Solve the puzzle it shows you (this proves you are a person)
6. GitHub emails you an **8-digit code**. Open your email, copy it, paste it in
7. When it asks about a plan, choose the **free** option. Free is enough for
   everything in this workshop and far beyond

### What a repository is

You will see the word "repository" (usually shortened to **repo**) everywhere.

A repository is just **one project's folder, stored on GitHub, with all of its
history**. One project, one repo.

We create ours in Part 3. Nothing to do now.

---

## 0.7 A Render account

### What it is

Render is the company that will run our application on a computer that never
turns off. Their free plan needs **no credit card**.

We cover what Render actually is, and what the alternatives are, in Part 1.
Right now we are only creating the account.

### Creating one

1. Go to **<https://render.com>**
2. Click **Get Started** (or **Sign Up**)
3. Choose **Sign in with GitHub**

Signing in with GitHub means you do not create another password, and Render can
see the repositories you tell it to.

4. GitHub asks you to **Authorize Render**

> **What is that screen asking?**
>
> It is GitHub checking that you are happy for Render to read your code. This is
> normal and required — Render cannot deploy code it cannot read.
>
> Get into the habit of reading these screens rather than clicking through.
> Check the name of the app asking, and what access it wants. Here it should say
> Render, and it should be asking about repositories.

5. Choose the **free** plan when offered. No card is required

Nothing else to do here. We come back to it in Part 3.

---

## 0.8 One thing that will trip you up on Windows

Not now — in Part 2, when you activate a virtual environment. It is included
here so you recognise it when it happens.

You will run this:

```
.venv\Scripts\activate
```

and PowerShell may refuse:

```
.venv\Scripts\activate : File ... cannot be loaded because
running scripts is disabled on this system.
```

Nothing is broken. Windows blocks scripts by default as a security measure.

**The fix**, run once in PowerShell:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Type `Y` and press Enter. This allows scripts you wrote yourself, and scripts
that are signed. It applies only to your own user account, not the whole
machine.

Then try `.venv\Scripts\activate` again.

---

## 0.9 Checklist

Open a **new** terminal and run all four. Do not continue until each one prints
a version number.

```
python --version
```

```
pip --version
```

```
git --version
```

```
code --version
```

*(If `code --version` fails, that is the least important one — VS Code still
works, it just is not on your PATH. Everything else must work.)*

And confirm:

- [ ] File name extensions are visible in File Explorer
- [ ] You can open a folder in VS Code and use its built-in terminal
- [ ] You are logged in at github.com
- [ ] You are logged in at render.com

---

## If something will not work

| What you see | What it means | Fix |
|---|---|---|
| `python is not recognized` | the PATH checkbox was missed | reinstall Python, tick **Add python.exe to PATH** |
| `git is not recognized` | terminal opened before install | close the terminal, open a new one |
| Command seems to do nothing | wrong drive (Command Prompt) | type `E:` on its own first |
| `The system cannot find the path` | a space in the path | wrap it in quotes: `cd "My Folder"` |
| `running scripts is disabled` | Windows script blocking | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Your `.env` file is called `.env.txt` | extensions are hidden | turn on file extensions (section 0.2), rename it |
| macOS: `python: command not found` | macOS uses `python3` | use `python3` and `pip3` everywhere |

Still stuck? Note the **exact** error text and ask. The message almost always
names the problem, and reading it carefully is a skill worth building now.

---

Setup is done. **Part 1** explains what these technologies actually are, before
we write any code.
