import requests
import subprocess
import time

SERVER_URL = "http://localhost:5000"


def poll_for_task():
    # Poll the backend to get the next queued task
    response = requests.get(f"{SERVER_URL}/get-task")
    task = response.json()
    return task if task.get('task_id') else None


def run_task_with_podman(task):
    task_id = task['task_id']
    docker_image = task['docker_image']
    command = task['command']

    # Pull the container image in case it's not available locally
    subprocess.run(["podman", "pull", docker_image], check=True)

    # Run the container and capture its output
    result = subprocess.run(
        ["podman", "run", "--rm", docker_image] + command.split(),
        capture_output=True,
        text=True
    )
    stdout = result.stdout
    stderr = result.stderr

    if result.returncode != 0:
        print(f"Task {task_id} failed with error: {stderr}")
        return None, stderr

    return stdout, None


def upload_results(task_id, stdout, output_file=None):
    data = {'task_id': task_id, 'stdout': stdout}
    files = {'file': open(output_file, 'rb')} if output_file else None
    response = requests.post(f"{SERVER_URL}/upload-results", data=data, files=files)
    print(response.json())


if __name__ == "__main__":
    while True:
        print("Polling for new tasks...")
        task = poll_for_task()
        if task:
            print(f"Task received: {task}")
            stdout, error = run_task_with_podman(task)
            if stdout:
                print(f"Task output: {stdout}")
                upload_results(task['task_id'], stdout)
            else:
                print(f"Task error: {error}")
        time.sleep(5)
