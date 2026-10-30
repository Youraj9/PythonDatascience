import streamlit as st

from utils.catalogue import FLAT_TOPICS, MODULE_ONE_TOPICS
from utils.content import load_topic
from utils.progress import get_topic_status, update_topic_status

st.set_page_config(page_title="Lesson · Learn by Building", page_icon="🧠", layout="wide")
topic_id = st.query_params.get("topic", MODULE_ONE_TOPICS[0]["id"])
available = {topic["id"]: topic for topic in FLAT_TOPICS if topic["available"]}
if topic_id not in available:
    topic_id = MODULE_ONE_TOPICS[0]["id"]

selected = st.selectbox(
    "Module 1 topic",
    list(available),
    index=list(available).index(topic_id),
    format_func=lambda key: available[key]["title"],
)
topic = available[selected]
data = load_topic(selected)
st.title(data["title"])
st.caption(f'{topic["module"]} · {topic["difficulty"]}')
st.markdown(data["lesson"])

with st.expander("Runnable example"):
    st.code(data["example"], language="python")

st.subheader("Common mistakes")
for mistake in data["mistakes"]:
    st.markdown(f"- {mistake}")

st.info(f'**Keep in mind:** {data["keep_in_mind"]}', icon="💡")

st.subheader("Interview questions")
for question in data["interview_questions"]:
    st.markdown(f"- {question}")

if get_topic_status(selected) != "Done":
    if st.button("Mark topic complete"):
        update_topic_status(selected, "Done")
        st.success("Progress saved.")
        st.rerun()
else:
    st.success("Topic complete")

practice_col, quiz_col = st.columns(2)
with practice_col:
    if st.button("Practice this topic"):
        st.query_params["topic"] = selected
        st.switch_page("pages/3_Practice.py")
with quiz_col:
    if st.button("Take the topic quiz"):
        st.query_params["topic"] = selected
        st.switch_page("pages/4_Quiz.py")
