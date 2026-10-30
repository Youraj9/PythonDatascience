# Learn by Building

A local, multipage Streamlit learning app for modern Python, data science, machine learning, and fintech. It teaches with short explanations, runnable examples, practice, and quizzes.

## Run locally

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. Progress is stored in `data/progress.sqlite3`; it stays on this machine.

## Structure

- `app.py`: home dashboard and diagnostic
- `pages/`: catalogue, lessons, practice, quizzes, and guided projects
- `pages/6_Model_Lab.py`: interactive logistic-regression probability demo
- `.streamlit/config.toml`: app theme and local-server defaults
- `content/catalogue.json`: complete topic map and module availability
- `content/python_modern/`: one content file per Module 1 topic
- `content/data_science/`, `content/machine_learning/`, `content/fintech/`: one queued lesson file per later topic
- `exercises/`: exercise organization notes
- `utils/`: SQLite progress, content loading, and exercise execution

The catalogue lists every requested curriculum area. Module 1 covers the complete modern Python track; each of its nine topics has an individual content file, three practice levels, and three interview prompts. Data science, machine learning, and fintech lessons remain queued for the requested module-by-module test-and-build workflow.

## Practice runner safety

Practice submissions execute as local Python code in a subprocess with a three-second timeout. This is not a security sandbox: only run code you trust, and do not expose this app to untrusted users or the public internet.

## Datasets

Lessons use small illustrative examples. Later data-science and ML modules will use free built-in scikit-learn datasets and freely available Kaggle datasets where appropriate. Kaggle downloads may require a Kaggle account and API credentials.
