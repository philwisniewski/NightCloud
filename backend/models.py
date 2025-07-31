# backend/models.py

import sqlite3


DB_PATH = "database.db"


def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        docker_image TEXT,
                        command TEXT,
                        status TEXT DEFAULT 'queued'
                      )""")
    conn.commit()
    conn.close()


def save_task(docker_image, command):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (docker_image, command) VALUES (?, ?)",
                   (docker_image, command))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_task():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, docker_image, command FROM tasks WHERE status='queued' LIMIT 1")
    task = cursor.fetchone()
    if task:
        cursor.execute("UPDATE tasks SET status='running' WHERE id=?", (task[0],))
        conn.commit()
        conn.close()
        return {"task_id": task[0], "docker_image": task[1], "command": task[2]}
    else:
        conn.close()
        return None


def update_task_status(task_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()
