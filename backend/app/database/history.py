import sqlite3
from pathlib import Path

DB_PATH = Path("data/reviewguard.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repository TEXT,
        review_date TEXT,
        score INTEGER,
        grade TEXT,
        risk TEXT,
        findings INTEGER,
        approved INTEGER,
        summary TEXT,
        feedback TEXT,
        review_id TEXT
    )
    """)

    conn.commit()
    conn.close()

from datetime import datetime


def save_review(state):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO reviews (
            repository,
            review_date,
            score,
            grade,
            risk,
            findings,
            approved,
            summary,
            feedback,
            review_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            state["repo_path"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            state["score"],
            state["grade"],
            state["risk"],
            len(state["findings"]),
            int(state.get("human_approved", 1)),
            state.get("summary", ""),
            state.get("reviewer_feedback", ""),
            state.get("review_id", ""),
        ),
    )

    conn.commit()
    conn.close()

def get_reviews():
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM reviews
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return rows