# os_kernel.py
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class MemoryManager:
    def __init__(self, db_path="agentos.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            user_id TEXT,
            content TEXT
        )
        """)
        self.conn.commit()

    def save(self, user_id, content):
        self.conn.execute(
            "INSERT INTO memory VALUES (?, ?)", (user_id, content)
        )
        self.conn.commit()

    def recall(self, user_id):
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM memory WHERE user_id=?", (user_id,))
        rows = cur.fetchall()
        return "\n".join(r[0] for r in rows[-5:])


class PermissionEngine:
    def verify(self, agent, tool):
        return True  # start simple (enterprise later)
    
def summarize(self, user_id):
    memories = self.recall(user_id)
    if len(memories) > 500:
        return memories[:300] + "...(summary)"
    return memories