import streamlit as st

from utils.catalogue import CATALOGUE, FLAT_TOPICS
from utils.progress import get_dashboard, get_topic_status, save_diagnostic

st.set_page_config(page_title="Learn by Building", page_icon="🧭", layout="wide")


def run_diagnostic() -> None:
    questions = [
        ("python", "Which annotation enforces a value's type at runtime?", ["A Python type hint", "Pydantic validation", "A dataclass", "An enum"], 1),
        ("python", "What does a decorator usually do?", ["Wrap or modify a callable", "Create a virtual environment", "Pause a thread", "Declare a class field"], 0),
        ("python", "Which tool is designed for Python unit testing?", ["pytest", "ruff", "uv", "httpx"], 0),
        ("data", "What does a Pandas DataFrame represent?", ["A labeled 2D table", "A neural network", "A SQL server", "A Python package"], 0),
        ("data", "Why should train and test data be split?", ["To estimate generalization on unseen data", "To make training faster in all cases", "To remove missing values", "To scale the features"], 0),
        ("ml", "What is data leakage?", ["Using information unavailable at prediction time", "A high training score", "A small dataset", "A model with few features"], 0),
        ("ml", "Which metric is often more informative than accuracy for rare fraud?", ["Recall", "R-squared", "RMSE", "Silhouette score"], 0),
        ("ml", "What does K-Means primarily do?", ["Groups observations into k clusters", "Predicts a numeric target", "Ranks search results", "Encodes categories"], 0),
        ("ml", "What is an embedding?", ["A vector representation of an item", "A type of database index", "A train/test split", "A loss function"], 0),
    ]
    answers = []
    with st.form("diagnostic_form"):
        st.write("Choose the best answer. This is a starting point, not a graded exam.")
        for i, (area, prompt, options, correct) in enumerate(questions):
            selected = st.radio(prompt, options, key=f"diagnostic_{i}")
            answers.append((area, options.index(selected) == correct))
        submitted = st.form_submit_button("Submit diagnostic")
    if submitted:
        scores = {}
        for area, correct in answers:
            scores[area] = scores.get(area, 0) + int(correct)
        save_diagnostic(scores)
        st.session_state["diagnostic_feedback"] = (
            f"Saved. Python: {scores.get('python', 0)}/3 · "
            f"Data: {scores.get('data', 0)}/2 · "
            f"ML: {scores.get('ml', 0)}/4"
        )


st.title("Learn by Building")
st.write("Your hands-on path from modern Python to machine learning. Learn a concept, see it in code, then practise it.")

dashboard = get_dashboard()
cols = st.columns(3)
cols[0].metric("Topics completed", dashboard["completed_topics"])
cols[1].metric("Latest quiz score", dashboard["latest_quiz"])
cols[2].metric("Learning streak", f'{dashboard["streak"]} days')

if dashboard["diagnostic"]:
    st.info(
        "Your catalogue is prioritized from your diagnostic: "
        + ", ".join(f"{area.title()} {score}/{total}" for area, (score, total) in dashboard["diagnostic"].items())
    )
else:
    st.subheader("Start with a short diagnostic")
    st.caption("Your results prioritize topics where you may want more practice. You can still study in any order.")
    run_diagnostic()
    if st.session_state.get("diagnostic_feedback"):
        st.success(st.session_state["diagnostic_feedback"])

st.subheader("Learning path")
for module in CATALOGUE:
    topics = module["topics"]
    completed = sum(get_topic_status(topic["id"]) == "Done" for topic in topics)
    st.write(f"**{module['title']}** — {completed}/{len(topics)} topics completed")
    st.progress(completed / len(topics) if topics else 0)

st.subheader("Explore a live model")
st.write("Change the weight, bias, and decision threshold to see a logistic regression curve move.")
if st.button("Open the interactive model lab"):
    st.switch_page("pages/6_Model_Lab.py")

if dashboard["recent_quizzes"]:
    st.subheader("Recent quiz scores")
    for topic_id, score, total, completed_at in dashboard["recent_quizzes"]:
        st.write(f"- **{topic_id.replace('_', ' ').title()}** — {score}/{total} · {completed_at}")

st.caption(f"{len(FLAT_TOPICS)} topics are mapped in the catalogue. Module 1 is ready to study; later modules will be authored one at a time.")
