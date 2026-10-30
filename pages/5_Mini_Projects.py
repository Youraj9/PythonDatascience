import streamlit as st

from utils.progress import get_checklist, save_checklist_item

st.set_page_config(page_title="Mini-projects · Learn by Building", page_icon="🛠️", layout="wide")
st.title("Mini-projects")
st.caption("Guided projects unlock alongside their learning modules.")

projects = [
    ("type-safe-config", "Type-safe app configuration", "Build a validated configuration model with a dataclass, enum, and Pydantic model.", ["Define the accepted environment values", "Model and validate configuration", "Add tests for invalid input"]),
    ("credit-risk", "Credit-risk starter", "Later project · compare a baseline classifier with a leakage-safe evaluation.", ["Frame the target and prediction point", "Prepare a train/test split", "Compare recall and precision"]),
    ("fraud-monitor", "Fraud-detection monitor", "Later project · explore class imbalance and monitor changes in transaction data.", ["Inspect class balance", "Set an evaluation threshold", "Sketch a drift check"]),
]
for project_id, title, description, steps in projects:
    with st.expander(title):
        st.write(description)
        if project_id != "type-safe-config":
            st.info("This project will be expanded in a later module.")
        checked = get_checklist(project_id)
        for index, step in enumerate(steps):
            value = st.checkbox(step, value=index in checked, key=f"{project_id}_{index}")
            save_checklist_item(project_id, index, value)
