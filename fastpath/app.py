"""The whole application. No HTML, no server code, no deployment config.

    pip install gradio scikit-learn joblib
    python app.py
"""
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
