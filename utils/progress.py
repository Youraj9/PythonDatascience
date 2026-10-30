import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "progress.sqlite3"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS topic_progress (
            topic_id TEXT PRIMARY KEY,
            status TEXT NOT NULL CHECK(status IN ('Not started', 'In progress', 'Done')),
            updated_at TEXT NOT NULL
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS activity (
            activity_date TEXT PRIMARY KEY
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS diagnostics (
            area TEXT PRIMARY KEY,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS project_checklist (
            project_id TEXT NOT NULL,
            item_index INTEGER NOT NULL,
            checked INTEGER NOT NULL,
            PRIMARY KEY(project_id, item_index)
        )"""
    )
    return connection


def _record_activity(connection: sqlite3.Connection) -> None:
    connection.execute("INSERT OR IGNORE INTO activity(activity_date) VALUES (?)", (date.today().isoformat(),))


def get_topic_status(topic_id: str) -> str:
    with _connect() as connection:
        row = connection.execute("SELECT status FROM topic_progress WHERE topic_id = ?", (topic_id,)).fetchone()
    return row[0] if row else "Not started"


def update_topic_status(topic_id: str, status: str) -> None:
    if status not in {"Not started", "In progress", "Done"}:
        raise ValueError(f"Invalid topic status: {status}")
    with _connect() as connection:
        connection.execute(
            """INSERT INTO topic_progress(topic_id, status, updated_at) VALUES (?, ?, ?)
            ON CONFLICT(topic_id) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at""",
            (topic_id, status, date.today().isoformat()),
        )
        _record_activity(connection)


def save_quiz_score(topic_id: str, score: int, total: int) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT INTO quiz_scores(topic_id, score, total, created_at) VALUES (?, ?, ?, ?)",
            (topic_id, score, total, date.today().isoformat()),
        )
        _record_activity(connection)


def save_diagnostic(scores: dict[str, int]) -> None:
    totals = {"python": 3, "data": 2, "ml": 4}
    with _connect() as connection:
        for area, score in scores.items():
            connection.execute(
                """INSERT INTO diagnostics(area, score, total, created_at) VALUES (?, ?, ?, ?)
                ON CONFLICT(area) DO UPDATE SET score=excluded.score, total=excluded.total, created_at=excluded.created_at""",
                (area, score, totals[area], date.today().isoformat()),
            )
        _record_activity(connection)


def get_diagnostic() -> dict[str, tuple[int, int]]:
    with _connect() as connection:
        rows = connection.execute("SELECT area, score, total FROM diagnostics").fetchall()
    return {area: (score, total) for area, score, total in rows}


def get_checklist(project_id: str) -> set[int]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT item_index FROM project_checklist WHERE project_id = ? AND checked = 1", (project_id,)
        ).fetchall()
    return {row[0] for row in rows}


def save_checklist_item(project_id: str, index: int, checked: bool) -> None:
    with _connect() as connection:
        connection.execute(
            """INSERT INTO project_checklist(project_id, item_index, checked) VALUES (?, ?, ?)
            ON CONFLICT(project_id, item_index) DO UPDATE SET checked=excluded.checked""",
            (project_id, index, int(checked)),
        )
        if checked:
            _record_activity(connection)


def get_dashboard() -> dict:
    with _connect() as connection:
        completed = connection.execute("SELECT COUNT(*) FROM topic_progress WHERE status = 'Done'").fetchone()[0]
        latest = connection.execute(
            "SELECT score, total FROM quiz_scores ORDER BY id DESC LIMIT 1"
        ).fetchone()
        recent_quizzes = connection.execute(
            "SELECT topic_id, score, total, created_at FROM quiz_scores ORDER BY id DESC LIMIT 5"
        ).fetchall()
        dates = {
            date.fromisoformat(row[0])
            for row in connection.execute("SELECT activity_date FROM activity").fetchall()
        }
    streak = 0
    day = date.today() if date.today() in dates else date.today() - timedelta(days=1)
    while day in dates:
        streak += 1
        day -= timedelta(days=1)
    diagnostic = get_diagnostic()
    return {
        "completed_topics": completed,
        "latest_quiz": f"{latest[0]}/{latest[1]}" if latest else "—",
        "recent_quizzes": recent_quizzes,
        "streak": streak,
        "diagnostic": diagnostic,
    }
