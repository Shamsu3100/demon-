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

## The five parts

| Part | What it covers | Code? |
|---|---|---|
| **0** | Setting up your computer, from nothing | no |
| **1** | What these technologies actually are | no |
| **2** | Building the application, in five stages | yes |
| **3** | Putting it on the internet | yes |
| **4** | Where to go next | yes |

**Parts 0 and 1 contain no code.** If you already have Python, VS Code and Git
working, and you know what a server and an API are, start at Part 2.

## The companion repository

**<https://github.com/Shamsu3100/demon->**

Every stage of Part 2 exists there as a complete, working folder:

```
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
