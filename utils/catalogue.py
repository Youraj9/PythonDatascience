import json
from pathlib import Path

from utils.progress import get_diagnostic, get_topic_status

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = json.loads((ROOT / "content" / "catalogue.json").read_text(encoding="utf-8"))
MODULE_ONE_TOPICS = [topic for topic in CATALOGUE[0]["topics"] if topic["available"]]
FLAT_TOPICS = [
    {**topic, "module": module["title"], "module_id": module["id"]}
    for module in CATALOGUE
    for topic in module["topics"]
]


def get_prioritized_topics() -> list[dict]:
    topics = []
    for topic in FLAT_TOPICS:
        topics.append({**topic, "status": get_topic_status(topic["id"])})
    diagnostic = get_diagnostic()
    if not diagnostic:
        return topics
    priority = {"python": 0, "data": 1, "ml": 2}
    area_for_module = {}
    for module in CATALOGUE:
        area_for_module[module["id"]] = module["area"]
    return sorted(
        topics,
        key=lambda topic: (
            -(
                diagnostic.get(area_for_module[topic["module_id"]], (0, 0))[1]
                - diagnostic.get(area_for_module[topic["module_id"]], (0, 0))[0]
            ),
            priority[area_for_module[topic["module_id"]]],
            topic["title"],
        ),
    )
