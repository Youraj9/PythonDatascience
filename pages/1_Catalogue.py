import streamlit as st

from utils.catalogue import get_prioritized_topics
from utils.progress import get_topic_status, update_topic_status

st.set_page_config(page_title="Catalogue · Learn by Building", page_icon="📚", layout="wide")
st.title("Catalogue")
st.write("Search the complete learning path, filter by level, and track each topic.")

query = st.text_input("Search topics and modules")
levels = ["Beginner", "Intermediate", "Advanced"]
selected_levels = st.multiselect("Difficulty", levels, default=levels)
topics = get_prioritized_topics()
rows = []
for topic in topics:
    status = get_topic_status(topic["id"])
    if query.lower() not in f'{topic["title"]} {topic["module"]} {topic["description"]}'.lower():
        continue
    if topic["difficulty"] not in selected_levels:
        continue
    rows.append((topic, status))

if not rows:
    st.info("No topics match these filters.")

for topic, status in rows:
    with st.container(border=True):
        left, middle, right = st.columns([5, 2, 2])
        with left:
            st.subheader(topic["title"])
            st.caption(f'{topic["module"]} · {topic["description"]}')
        with middle:
            st.markdown(f'**{topic["difficulty"]}**')
            st.caption(f"Status: {status}")
        with right:
            if topic["available"]:
                if st.button("Open lesson", key=f'open_{topic["id"]}'):
                    st.query_params["topic"] = topic["id"]
                    st.switch_page("pages/2_Lesson.py")
            else:
                st.button("Coming in a later module", key=f'locked_{topic["id"]}', disabled=True)
        new_status = st.selectbox(
            "Progress",
            ["Not started", "In progress", "Done"],
            index=["Not started", "In progress", "Done"].index(status),
            key=f'status_{topic["id"]}',
            label_visibility="collapsed",
        )
        if new_status != status:
            update_topic_status(topic["id"], new_status)
            st.rerun()
