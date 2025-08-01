document.getElementById('task-form').onsubmit = async function(event) {
    event.preventDefault();

    const dockerImage = document.getElementById('docker-image').value;
    const command = document.getElementById('command').value;

    const response = await fetch('http://127.0.0.1:5000/submit-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docker_image: dockerImage, command: command }),
    });

    const data = await response.json();
    alert(`Task submitted: ${data.task_id}`);

    loadTasks();
};

async function loadTasks() {
    const response = await fetch('http://127.0.0.1:5000/list-tasks');
    const tasks = await response.json();

    const table = document.getElementById('task-table');

    table.innerHTML = `
      <tr>
        <th>Task ID</th>
        <th>Status</th>
        <th>Output</th>
      </tr>
    `;

    for (const task of tasks) {
        const row = table.insertRow();
        row.insertCell(0).innerText = task.task_id;
        row.insertCell(1).innerText = task.status;
        row.insertCell(2).innerText = task.status === "completed"
          ? `See outputs/${task.task_id}_stdout.txt`
          : '';
    }
}

loadTasks();
