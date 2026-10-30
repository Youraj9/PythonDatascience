import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_topic(topic_id: str) -> dict:
    path = ROOT / "content" / "python_modern" / f"{topic_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Lesson content is not available for topic: {topic_id}")
    return json.loads(path.read_text(encoding="utf-8"))
