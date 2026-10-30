import math

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Model Lab · Learn by Building", page_icon="📈", layout="wide")
st.title("Interactive Model Lab")
st.write("Explore how a logistic regression model turns a transaction signal into a probability.")

with st.sidebar:
    st.subheader("Model controls")
    weight = st.slider("Feature weight", min_value=-3.0, max_value=3.0, value=1.0, step=0.1)
    bias = st.slider("Bias", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
    threshold = st.slider("Decision threshold", min_value=0.05, max_value=0.95, value=0.5, step=0.05)

scores = [-6.0 + index for index in range(13)]
probabilities = [
    1 / (1 + math.exp(-max(-60.0, min(60.0, weight * score + bias))))
    for score in scores
]
chart_data = pd.DataFrame(
    {
        "Feature score": scores,
        "Fraud probability": probabilities,
        "Decision threshold": [threshold] * len(scores),
    }
)
st.line_chart(chart_data, x="Feature score", y=["Fraud probability", "Decision threshold"])

prediction = 1 / (1 + math.exp(-max(-60.0, min(60.0, weight + bias))))
metric_columns = st.columns(3)
metric_columns[0].metric("Probability at score 1", f"{prediction:.1%}")
metric_columns[1].metric("Threshold", f"{threshold:.0%}")
metric_columns[2].metric("Illustrative prediction", "Flag" if prediction >= threshold else "Review")

st.markdown(
    """
### How to read the plot

The S-shaped curve is the model's estimated probability as a feature score changes.
The **weight** controls its direction and steepness, the **bias** shifts the curve,
and the **threshold** changes where a probability becomes a positive classification.
In real fraud detection, thresholds should reflect the cost of missed fraud and
false alerts—not default to 50% automatically.
"""
)
st.info(
    "This is a synthetic teaching demo, not a trained model or financial advice. "
    "Real transactions require a representative dataset, time-aware validation, "
    "careful threshold selection, and ongoing monitoring."
)
