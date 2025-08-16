from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Dict, Any

DB_PATH = Path("data/processed/polls.sqlite")

SCHEMA_SQL = """
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    pollster TEXT,
    client TEXT,
    fieldwork_start DATE,
    fieldwork_end DATE,
    publish_date DATE,
    sample_size INTEGER,
    population TEXT,
    url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS poll_results (
    poll_id INTEGER NOT NULL,
    party TEXT NOT NULL,
    percent REAL,
    FOREIGN KEY (poll_id) REFERENCES polls(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_polls_dates ON polls(fieldwork_end, publish_date);
CREATE INDEX IF NOT EXISTS idx_results_party ON poll_results(party);
"""

def get_conn(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path.as_posix())
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()

def insert_poll(conn: sqlite3.Connection, meta: Dict[str, Any], results: Dict[str, float]) -> int:
    cur = conn.cursor()
    cols = [k for k in meta.keys()]
    placeholders = ",".join(["?"] * len(cols))
    cur.execute(f"INSERT INTO polls ({','.join(cols)}) VALUES ({placeholders})", tuple(meta[k] for k in cols))
    poll_id = cur.lastrowid
    cur.executemany(
        "INSERT INTO poll_results (poll_id, party, percent) VALUES (?, ?, ?)",
        [(poll_id, p, float(v) if v is not None else None) for p, v in results.items()]
    )
    conn.commit()
    return poll_id
