# backend/models.py

import sqlite3


DB_PATH = "database.db"


def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sub TEXT UNIQUE, -- OIDC subject claim
        name TEXT
    )"""
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        docker_image TEXT,
        command TEXT,
        status TEXT DEFAULT 'queued',
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )"""
    )
    conn.commit()
    conn.close()


def get_task():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, docker_image, command FROM tasks WHERE status='queued' LIMIT 1"
    )
    task = cursor.fetchone()
    if task:
        cursor.execute("UPDATE tasks SET status='running' WHERE id=?", (task[0],))
        conn.commit()
        conn.close()
        return {"task_id": task[0], "docker_image": task[1], "command": task[2]}
    else:
        conn.close()
        return None


def get_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, status FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return [{"task_id": row[0], "status": row[1]} for row in tasks]


def update_task_status(task_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()


def get_or_create_user(sub, name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE sub=?", (sub,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return {"id": user[0]}
    cursor.execute("INSERT INTO users (sub, name) VALUES (?, ?)", (sub, name))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id}


def save_task(docker_image, command, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (docker_image, command, user_id) VALUES (?, ?, ?)",
        (docker_image, command, user_id),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_tasks_for_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, status FROM tasks WHERE user_id=? ORDER BY id DESC", (user_id,)
    )
    tasks = cursor.fetchall()
    conn.close()
    return [{"task_id": row[0], "status": row[1]} for row in tasks]


def user_owns_task(user_id, task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id=? AND user_id=?", (task_id, user_id))
    task = cursor.fetchone()
    conn.close()
    return bool(task)
