import streamlit as st

from utils.catalogue import MODULE_ONE_TOPICS
from utils.content import load_topic
from utils.progress import save_quiz_score

st.set_page_config(page_title="Quiz · Learn by Building", page_icon="✅", layout="wide")
topic_ids = [topic["id"] for topic in MODULE_ONE_TOPICS]
topic_id = st.query_params.get("topic", topic_ids[0])
if topic_id not in topic_ids:
    topic_id = topic_ids[0]
selected = st.selectbox(
    "Topic",
    topic_ids,
    index=topic_ids.index(topic_id),
    format_func=lambda key: next(topic["title"] for topic in MODULE_ONE_TOPICS if topic["id"] == key),
)
topic = load_topic(selected)
st.title(f'Quiz: {topic["title"]}')
questions = topic["quiz"]
with st.form(f"quiz_{selected}"):
    answers = []
    for i, question in enumerate(questions):
        if question["type"] == "mcq":
            answer = st.radio(question["question"], question["options"], key=f"quiz_{selected}_{i}")
        else:
            answer = st.text_input(question["question"], key=f"quiz_{selected}_{i}")
        answers.append(answer)
    submitted = st.form_submit_button("Check answers")

if submitted:
    score = 0
    for question, answer in zip(questions, answers):
        if question["type"] == "mcq":
            correct = answer == question["options"][question["answer_index"]]
        else:
            normalized = answer.casefold()
            correct = all(term.casefold() in normalized for term in question["expected_terms"])
        score += int(correct)
        if correct:
            st.success(f'Correct — {question["explanation"]}')
        else:
            st.error(f'Not quite — {question["explanation"]}')
    save_quiz_score(selected, score, len(questions))
    st.metric("Score", f"{score}/{len(questions)}")
