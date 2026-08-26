"""The same model, presented with Streamlit instead of Gradio.

    pip install streamlit scikit-learn joblib
    streamlit run streamlit_app.py

Deployed free on Streamlit Community Cloud, which reads from a GitHub
repository.
"""
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

if st.button("Check reading", type="primary"):
    span = (high - low) or 1
    position = (value - low) / span          # the same feature used in training
    severity = model.predict([[position]])[0]

    st.markdown(f"### :{SEVERITY_COLOUR[severity]}[{severity.upper()}]")
    st.write(SEVERITY_NOTE[severity])
    st.caption(f"position in range: {position:.2f}  "
               f"(0.0 = lowest, 1.0 = highest)")
