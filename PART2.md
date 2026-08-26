# Part 2 — The fast path

**You will have something on the internet in about twenty minutes.**

This part uses no HTML, no server code, and no deployment configuration. If you
have never deployed anything, start here — you will have a working public link
before we build the fuller version in Part 3.

If you are already comfortable with web development, read it anyway. Knowing
when this path is enough will save you days.

---

## 2.1 The situation this solves

Most student projects end here:

```
   a notebook that works    →    on one laptop    →    nobody else can use it
```

You trained a model. It works. It lives in a `.ipynb` file, and the only way
anyone else sees it is if they sit next to you.

The fast path turns that into a web address, in three steps:

```
   train_model.ipynb   →   model.pkl   →   app.py   →   a public URL
      (train it)         (save it)      (wrap it)     (share it)
```

---

## 2.2 Step 1 — Get the model out of the notebook

The companion repository has `fastpath/train_model.ipynb`. Open it and run every
cell.

It does four things, and they are the four things every training notebook does:

| Cell | What it does |
|---|---|
| make data | 3,000 example readings with known answers |
| choose a feature | *where* the reading sits in its safe range, as one number |
| train | a decision tree learns the pattern |
| **save** | **`joblib.dump(model, "model.pkl")`** |

That last line is the important one.

```python
joblib.dump(model, "model.pkl")
```

> **`model.pkl` IS the model.** It is a file, about two kilobytes, and it is the
> only thing that needs to leave your notebook. Everything above that line ran
> once and never runs again.
>
> This is the step people miss. A notebook is where you *make* a model. It is
> not where the model lives afterwards.

If you have your own trained model from another workshop, save it the same way
and skip to the next step.

### A note on the feature

The notebook does not give the model three raw numbers. It gives it one:

```python
position = (value - low) / (high - low)
```

0.0 means the reading is at the bottom of its safe range, 1.0 at the top,
negative means below it, above 1.0 means over it.

That single number lets one model handle a body temperature of 37 °C and a motor
temperature of 87 °C without being confused by the difference in scale. Choosing
what to feed a model matters more than which model you choose.

---

## 2.3 Step 2 — Wrap it in an interface

Create `app.py` next to `model.pkl`:

```python
import gradio as gr
import joblib

model = joblib.load("model.pkl")


def check_reading(value, low, high):
    """Runs when someone presses the button."""
    span = (high - low) or 1
    position = (value - low) / span            # the same feature we trained on
    severity = model.predict([[position]])[0]

    note = {
        "normal":   "Inside the safe range.",
        "warning":  "Outside the safe range. Worth checking.",
        "critical": "Far outside the safe range. Act now.",
    }[severity]
    return severity.upper(), note


demo = gr.Interface(
    fn=check_reading,
    inputs=[
        gr.Number(label="Reading", value=39.4),
        gr.Number(label="Safe range: lowest", value=36.1),
        gr.Number(label="Safe range: highest", value=37.2),
    ],
    outputs=[
        gr.Text(label="Severity"),
        gr.Text(label="What it means"),
    ],
    title="Sensor Triage",
    description="Enter a reading and its safe range. A trained model decides how serious it is.",
    examples=[
        [36.8, 36.1, 37.2],
        [39.4, 36.1, 37.2],
        [1450, 400, 1000],
        [8, 30, 70],
    ],
)

if __name__ == "__main__":
    demo.launch()
```

Install and run:

```
pip install gradio scikit-learn joblib
```

```
python app.py
```

Open <http://127.0.0.1:7860>.

**You have a working interface.** Input boxes, a button, results, and clickable
examples — from about thirty lines, with no HTML and no CSS.

> **What Gradio is doing:** you gave it a Python function and described its
> inputs and outputs. It built the web page for you.
>
> **Streamlit** does the same job with a different style of code. Either is a
> good choice. Gradio is slightly better suited to "one function, some inputs,
> some outputs", which is exactly what a model is.

---

## 2.4 Step 3 — Put it on the internet

**Hugging Face Spaces** hosts this kind of application free, with no credit card.

1. Create an account at **<https://huggingface.co/join>**
2. Go to **<https://huggingface.co/new-space>**
3. Give it a name, choose **Gradio**, choose the **free** hardware, click
   **Create Space**
4. On the **Files** tab, click **Add file → Upload files**
5. Upload three files:

```
app.py             your interface
model.pkl          your trained model
requirements.txt   what to install
```

`requirements.txt` is three lines:

```
gradio
scikit-learn
joblib
```

6. Wait about two minutes while it builds

**Your application is live**, at an address like:

```
https://huggingface.co/spaces/your-name/sensor-triage
```

Open it on your phone. Send it to someone.

> **No git, no terminal, no configuration file.** You uploaded three files
> through a web page. For a model demonstration, this is genuinely the fastest
> route that exists.

### The other rapid options

| | What it is | Note |
|---|---|---|
| **Hugging Face Spaces** | free hosting for Gradio and Streamlit apps | best fit for a model demo |
| **Streamlit Community Cloud** | free hosting for Streamlit apps | connects to GitHub instead of uploads |
| **Render** | free hosting for anything | what we use in Part 4 |
| **Vercel** | free hosting, strongest for JavaScript front ends | Python support is limited |

---

## 2.5 What this path cannot do

Everything above is real, and for some projects it is all you need. Be clear
about the ceiling before you commit to it.

| | Fast path (Gradio + Spaces) | Full path (Part 3) |
|---|---|---|
| Time to a public URL | **20 minutes** | about an hour |
| HTML or server code | **none** | some |
| A person can use it | **yes** | yes |
| **A device can send readings to it** | **no** | **yes** |
| Custom addresses your code controls | no | yes |
| Store results between visits | no | yes |
| Control how it looks | limited | complete |
| Another program can call it | awkward | yes, it is an API |

**The row that decides it is the middle one.**

Gradio builds a page for a *person* to fill in. It does not give you an address
a microcontroller can POST to. If your Project Nexus prototype has an ESP32
sending sensor readings, this path cannot receive them, and no amount of
configuration changes that.

### So which should you use?

**Use the fast path if:**

- your project is a model, and people will type inputs into it
- you need something online today
- you are showing a capability rather than running a system

**Use the full path if:**

- hardware sends data to it
- you need to store results
- another program needs to call it
- you want control over the interface

**Many teams should do both.** The fast path is a good demonstration of your
model on its own. The full path is your actual prototype. They are not in
competition, and building the first one takes twenty minutes.

---

## 2.6 What you have now

```
   train_model.ipynb  ->  model.pkl  ->  app.py  ->  a public URL
```

You have taken a model out of a notebook and put it somewhere other people can
reach. That is the whole gap this workshop exists to close, and you have now
closed it once.

**Part 3 closes it the other way** — building a service that a device can talk
to, that stores what it receives, and that you control completely.
