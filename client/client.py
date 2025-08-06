import requests
import subprocess
import time

SERVER_URL = "http://127.0.0.1:5000"


def poll_for_task():
    # Poll the backend to get the next queued task
    response = requests.get(f"{SERVER_URL}/get-task")
    task = response.json()
    return task if task.get("task_id") else None


def run_task(task):
    task_id = task["task_id"]
    repo_url = task["repo_url"]

    print(f"Running task {task_id} for repo {repo_url}")
    subprocess.run(
        ["./run_task_in_lima.sh", repo_url, str(task_id)],
        check=True
    )

    subprocess.run(["podman", "pull", docker_image], check=True)

    return

if __name__ == "__main__":
    while True:
        print("Polling for new tasks...")
        task = poll_for_task()
        if task:
            print(f"Task received: {task}")
            run_task(task)
        time.sleep(5)
