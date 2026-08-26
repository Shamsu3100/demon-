---
title: ""
author: ""
date: ""
lang: en-GB
geometry: "a4paper, margin=2.4cm"
mainfont: "Cambria"
sansfont: "Calibri"
monofont: "Consolas"
fontsize: 11pt
linestretch: 1.15
colorlinks: true
linkcolor: "MidnightBlue"
urlcolor: "MidnightBlue"
toccolor: "black"
toc: true
toc-depth: 2
numbersections: false
---

# Why this workshop exists

Nine of the ten workshops in this series teach you to build something: a model,
a sensor rig, an algorithm, a circuit board.

**This is the one where somebody else gets to see it.**

```
   Your engineering idea            The other nine workshops
   --------------------            ------------------------
                                    a model . a sensor rig
                                    an algorithm . a PCB
              |                                |
              +----------------+---------------+
                               |
                               v
                 +-------------------------+
                 |  IT ALL LIVES ON ONE    |
                 |  LAPTOP                 |
                 +-------------------------+
                               |
                               v
                 +-------------------------+
                 |     THIS WORKSHOP       |
                 |   full-stack app        |
                 |   AI integration        |
                 |   cloud deployment      |
                 +-------------------------+
                               |
                               v
                     a link you can send
```

A trained model is invisible to anyone not sitting at the laptop that trained
it. A sensor reading in a terminal cannot be shown to a judge, a supervisor, or
a collaborator in another city.

This workshop is the bridge across that gap. It is not about AI, and it is not
about hardware. It is about the step that turns either one into something with
an address.

---

# How to use this guide

This guide takes you from a computer with nothing installed to a working web
application running at a public address that anyone can open.

**You do not need any prior experience of web development, servers, or
deployment.** You do need to be able to program — if you have written Python, C
for a microcontroller, or anything similar, you have enough.

## What you will build

A **sensor triage service**. Something sends a reading; your code decides
whether it is safe; an AI writes a short explanation; the result is stored and
displayed on a web page.

That shape fits every Project Nexus track, because every track measures a number
that should stay inside a range — a body temperature, a CO2 level, a soil
moisture percentage, a motor temperature.

## What it costs

Nothing. No API key, no credit card, no paid account. The application runs fully
in a mode that needs no AI service, and the hosting we use has a free tier that
does not ask for a card.

If you do have an AI key, a section shows you how to use it, and what it costs.
(Roughly one tenth of a cent per request.)

## The six parts

| Part | What it covers | Code? |
|---|---|---|
| **0** | Setting up your computer, from nothing | no |
| **1** | What these technologies actually are | no |
| **2** | **The fast path** — a model out of a notebook and online in 20 minutes | yes |
| **3** | Building the full application, in five stages | yes |
| **4** | Putting it on the internet | yes |
| **5** | Where to go next | yes |

**Parts 0 and 1 contain no code.** If you already have Python, VS Code and Git
working, and you know what a server and an API are, start at Part 2.

**There are two paths, and they are both real.** Part 2 gets a trained model
online in about twenty minutes with no HTML and no server code. Part 3 builds a
full application that a device can send readings to. Which you need depends on
your project, and Part 2 ends with a table that decides it.

## The companion repository

**<https://github.com/Shamsu3100/demon->**

The fast path lives in `fastpath/`, and every stage of Part 3 is a complete,
working folder:

```
fastpath/         the notebook, the model, and the Gradio app
stages/stage1     a server that answers
stages/stage2     the web page appears
stages/stage3     your code decides
stages/stage4     the readings are stored
stages/stage5     the AI explains
stages/stage6     the deployment files added
```

**If you fall behind, copy the stage you need and carry on.** You do not have to
start again.

Every line of code in this guide was run and tested before it was printed here.

## How to read the boxes

> Boxes like this one explain a term, warn about a trap, or give a piece of
> context. They are not optional extras — several of them describe mistakes that
> cost a full day if you meet them unprepared.

\newpage
