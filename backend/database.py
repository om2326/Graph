import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "app.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        row_count INTEGER NOT NULL,
        columns TEXT NOT NULL,
        is_default INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id TEXT NOT NULL,
        row_index INTEGER NOT NULL,
        data_json TEXT NOT NULL,
        FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_records_dataset ON records(dataset_id)")

    conn.commit()
    conn.close()

def get_all_datasets() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, row_count, columns, is_default, created_at FROM datasets ORDER BY is_default DESC, created_at DESC")
    rows = cursor.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "row_count": r["row_count"],
            "columns": json.loads(r["columns"]),
            "is_default": bool(r["is_default"]),
            "created_at": r["created_at"]
        })
    conn.close()
    return results

def get_dataset(dataset_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, row_count, columns, is_default, created_at FROM datasets WHERE id = ?", (dataset_id,))
    r = cursor.fetchone()
    if not r:
        conn.close()
        return None
    res = {
        "id": r["id"],
        "name": r["name"],
        "description": r["description"],
        "row_count": r["row_count"],
        "columns": json.loads(r["columns"]),
        "is_default": bool(r["is_default"]),
        "created_at": r["created_at"]
    }
    conn.close()
    return res

def get_dataset_records(dataset_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT data_json FROM records WHERE dataset_id = ? ORDER BY row_index ASC", (dataset_id,))
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(r["data_json"]) for r in rows]

def insert_dataset(dataset_id: str, name: str, description: str, columns: List[str], records: List[Dict[str, Any]], is_default: bool = False):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR REPLACE INTO datasets (id, name, description, row_count, columns, is_default) VALUES (?, ?, ?, ?, ?, ?)",
        (dataset_id, name, description, len(records), json.dumps(columns), 1 if is_default else 0)
    )
    
    cursor.execute("DELETE FROM records WHERE dataset_id = ?", (dataset_id,))
    
    record_tuples = [
        (dataset_id, idx, json.dumps(row))
        for idx, row in enumerate(records)
    ]
    cursor.executemany(
        "INSERT INTO records (dataset_id, row_index, data_json) VALUES (?, ?, ?)",
        record_tuples
    )
    
    conn.commit()
    conn.close()

def delete_dataset(dataset_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_default FROM datasets WHERE id = ?", (dataset_id,))
    row = cursor.fetchone()
    if not row or row["is_default"] == 1:
        conn.close()
        return False  # Cannot delete default preset
    cursor.execute("DELETE FROM datasets WHERE id = ?", (dataset_id,))
    cursor.execute("DELETE FROM records WHERE dataset_id = ?", (dataset_id,))
    conn.commit()
    conn.close()
    return True
