console.log("App.js loaded!");

const serverUrl = 'http://127.0.0.1:5000';

document.getElementById('login-btn').onclick = () => {
  console.log("Login clicked!");
  window.location.href = `${serverUrl}/login`;
};

document.getElementById('logout-btn').onclick = async () => {
  await fetch(`${serverUrl}/logout`, {
    method: 'GET',
    credentials: 'include',
  });
  window.location.href = 'http://127.0.0.1:8000';
};

document.getElementById('task-form').onsubmit = async function(event) {
  event.preventDefault();

  const dockerImage = document.getElementById('docker-image').value;
  const command = document.getElementById('command').value;

  const response = await fetch(`${serverUrl}/submit-task`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',  // important: send cookies
    body: JSON.stringify({ docker_image: dockerImage, command: command }),
  });

  if (response.status === 401) {
    alert("Please login first!");
    return;
  }

  const data = await response.json();
  alert(`Task submitted: ${data.task_id}`);
  loadTasks();
};

async function loadTasks() {
  const response = await fetch(`${serverUrl}/list-tasks`, { credentials: 'include' });
  if (!response.ok) return; // probably not logged in
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
    row.insertCell(2).innerHTML = task.status === "completed"
      ? `<a href="${serverUrl}/download-stdout/${task.task_id}" target="_blank">Download stdout</a>`
      : '';
  }
}

async function checkLogin() {
  const res = await fetch(`${serverUrl}/me`, { credentials: 'include' });
  if (res.ok) {
    const user = await res.json();
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'inline';
    document.getElementById('user-info').innerText = `Hello, ${user.name}`;
    document.getElementById('task-form').style.display = 'block';
    loadTasks();
  } else {
    document.getElementById('login-btn').style.display = 'inline';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('user-info').innerText = '';
    document.getElementById('task-form').style.display = 'none';
  }
}

// run on page load
checkLogin();

// optional auto-refresh tasks every 5s
setInterval(loadTasks, 5000);

