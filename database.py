
import sqlite3

def init_db():
    conn = sqlite3.connect("traffic.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            road_name TEXT NOT NULL,
            vehicle_count INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_road_time
        ON traffic (road_name, timestamp)
    """)

    conn.commit()
    conn.close()
