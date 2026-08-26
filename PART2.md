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

## 2.3 Step 2 — Wrap the model in an interface

Two libraries do this job. Both take a Python function and build a web page
around it. Choose either; the model file and everything before this point is
identical.

### Option A — Gradio

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

```
pip install gradio scikit-learn joblib
```

```
python app.py
```

Open <http://127.0.0.1:7860>.

### Option B — Streamlit

Create `streamlit_app.py`:

```python
import joblib
import streamlit as st

model = joblib.load("model.pkl")

SEVERITY_NOTE = {
    "normal":   "Inside the safe range.",
    "warning":  "Outside the safe range. Investigation recommended.",
    "critical": "Far outside the safe range. Immediate action required.",
}
SEVERITY_COLOUR = {"normal": "green", "warning": "orange", "critical": "red"}

st.title("Sensor Triage")
st.caption("Enter a reading and its safe operating range. "
           "A trained model determines the severity.")

value = st.number_input("Reading", value=39.4)
low = st.number_input("Safe range: lowest", value=36.1)
high = st.number_input("Safe range: highest", value=37.2)

# st.session_state survives re-runs, so the table below persists while the
# browser tab is open. It is NOT a database: refresh the page and it is gone.
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Check reading", type="primary"):
    span = (high - low) or 1
    position = (value - low) / span          # the same feature used in training
    severity = model.predict([[position]])[0]

    st.markdown(f"### :{SEVERITY_COLOUR[severity]}[{severity.upper()}]")
    st.write(SEVERITY_NOTE[severity])
    st.caption(f"position in range: {position:.2f}  "
               f"(0.0 = lowest, 1.0 = highest)")

    st.session_state.history.insert(0, {
        "Reading": value,
        "Safe range": f"{low} - {high}",
        "Position": round(position, 2),
        "Severity": severity,
    })

if st.session_state.history:
    st.divider()
    st.subheader("This session")
    st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)
    st.caption("Held in the browser session only. Refresh the page and it is lost. "
               "Storing readings properly requires a database, which is Part 3.")
```

```
pip install streamlit scikit-learn joblib
```

```
streamlit run streamlit_app.py
```

Open <http://localhost:8501>.

> **`st.session_state` is not a database.** It keeps the table while the browser
> tab is open, and loses it on refresh. That is enough to demonstrate a series of
> readings, and it is deliberately not enough to run a system on. Storing
> readings properly is Part 3.

### The difference between them

| | Gradio | Streamlit |
|---|---|---|
| Style | describe inputs and outputs, pass a function | write the page top to bottom |
| Best suited to | one function with fixed inputs — a model | dashboards, charts, several sections |
| Reruns | only your function, on submit | the whole script, on every interaction |
| Free hosting | Render, or Hugging Face Spaces (paid, see below) | **Streamlit Community Cloud** |

Both are good. **Streamlit currently has the better free hosting route**, which
is the deciding factor for this workshop.

> Note the `position` calculation appears in the training notebook and again in
> the application. Whatever you compute before training, you must compute again
> before predicting. Getting this wrong produces an application that runs
> perfectly and returns nonsense.

---

## 2.4 Step 3 — Deploy it

### The current free options

Checked August 2026. **Verify before you rely on any of them** — free tiers
change, sometimes without notice.

| | Runs | Free | Requires |
|---|---|---|---|
| **Streamlit Community Cloud** | Streamlit | **yes** | a GitHub repository |
| **Render** | either | **yes** | a GitHub repository |
| Hugging Face Spaces — Static | HTML only | yes | cannot run Python |
| Hugging Face Spaces — Gradio | Gradio | **no, paid plan** | — |
| Hugging Face Spaces — Docker | anything | **no, paid plan** | — |

> **Hugging Face Spaces changed.** It was the simplest route for a Gradio
> application: upload three files through a web page, no repository needed.
> Gradio and Docker Spaces now require a paid subscription. Only Static Spaces
> remain free, and those cannot run Python, so they cannot run a model.
>
> This is worth noticing as a general lesson rather than an inconvenience.
> **Free tiers move.** Anything you build should survive its host changing
> terms — which is an argument for keeping your model and your logic separate
> from whatever wraps them.

### Deploying to Streamlit Community Cloud

1. Put these three files in a GitHub repository:

```
streamlit_app.py     your interface
model.pkl            your trained model
requirements.txt     what to install
```

`requirements.txt`:

```
streamlit
scikit-learn
joblib
```

2. Go to **<https://share.streamlit.io>** and sign in with GitHub
3. Click **Create app**, then **Deploy a public app from GitHub**
4. Choose your repository, branch, and `streamlit_app.py` as the main file
5. Click **Deploy**

The build takes two to three minutes. Your application is then live at an
address ending in `.streamlit.app`.

**Limits:** approximately 1 GB of memory, and the application sleeps after
about 12 hours without visitors. That sleep window is considerably more
forgiving than most free hosting, which is useful for an exhibition.

### Deploying Gradio instead

Gradio is an ordinary Python web application, so any platform hosting Python
will run it — including Render, which we use in Part 4. Add a `render.yaml`
with:

```yaml
startCommand: python app.py
```

and set `server_name="0.0.0.0"` and `server_port` from the `PORT` environment
variable in `demo.launch()`. Part 4 covers what those two settings mean.

---

## 2.5 What this path cannot do

Everything above is real, and for some projects it is all you need. Be clear
about the ceiling before you commit to it.

| | Fast path (Gradio or Streamlit) | Full path (Part 3) |
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

Both Gradio and Streamlit build a page for a *person* to fill in. Neither gives you an address
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
