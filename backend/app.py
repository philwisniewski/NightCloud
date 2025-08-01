# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import initialize_db, save_task, get_task, get_all_tasks, update_task_status
import os

app = Flask(__name__)
CORS(app)
initialize_db()

UPLOAD_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/submit-task", methods=["POST"])
def submit_task():
    data = request.json
    docker_image = data.get("docker_image")
    command = data.get("command")
    task_id = save_task(docker_image, command)
    return jsonify({"task_id": task_id, "status": "Task submitted"})


@app.route("/get-task", methods=["GET"])
def get_task_api():
    task = get_task()
    if task:
        return jsonify(task)
    return jsonify({"message": "No tasks available"})


@app.route("/upload-results", methods=["POST"])
def upload_results():
    task_id = request.form["task_id"]
    stdout = request.form["stdout"]
    output_file = request.files.get("file")

    # save std out and files locally
    with open(f"{UPLOAD_FOLDER}/{task_id}_stdout.txt", "w") as f:
        f.write(stdout)

    file_path = None

    if output_file:
        file_path = f"{UPLOAD_FOLDER}/{task_id}_.output.zip"
        output_file.save(file_path)

    update_task_status(task_id, "completed")

    return jsonify({"message": "Results uploaded", "file_path": file_path})


@app.route("/list-tasks", methods=["GET"])
def list_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(debug=True)
