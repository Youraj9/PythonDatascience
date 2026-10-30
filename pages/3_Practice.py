import streamlit as st

from utils.catalogue import MODULE_ONE_TOPICS
from utils.content import load_topic
from utils.exercise_runner import run_exercise

st.set_page_config(page_title="Practice · Learn by Building", page_icon="⌨️", layout="wide")
topic_id = st.query_params.get("topic", MODULE_ONE_TOPICS[0]["id"])
topic_ids = [topic["id"] for topic in MODULE_ONE_TOPICS]
if topic_id not in topic_ids:
    topic_id = topic_ids[0]
selected = st.selectbox(
    "Topic",
    topic_ids,
    index=topic_ids.index(topic_id),
    format_func=lambda key: next(topic["title"] for topic in MODULE_ONE_TOPICS if topic["id"] == key),
)
topic = load_topic(selected)
st.title(f'Practice: {topic["title"]}')
st.warning("Code runs locally in a separate Python process with a time limit. Use this app only with code you trust; this is not a security sandbox.")

for index, exercise in enumerate(topic["exercises"]):
    with st.expander(f'{exercise["level"]}: {exercise["title"]}', expanded=index == 0):
        st.markdown(exercise["prompt"])
        if st.button("Show hint", key=f'hint_{selected}_{index}'):
            st.info(exercise["hint"])
        code = st.text_area(
            "Your code",
            value=exercise["starter"],
            height=220,
            key=f'code_{selected}_{index}',
            help="Implement the requested function. The tests check the function's return value.",
        )
        if st.button("Run tests", key=f'run_{selected}_{index}'):
            passed, result = run_exercise(code, exercise)
            if passed:
                st.success(result)
            else:
                st.error(result)
        with st.expander("Show solution"):
            st.code(exercise["solution"], language="python")
