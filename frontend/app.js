document.getElementById('task-form').onsubmit = async function(event) {
    event.preventDefault();

    const dockerImage = document.getElementById('docker-image').value;
    const command = document.getElementById('command').value;

    const response = await fetch('/submit-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docker_image: dockerImage, command: command }),
    });

    const data = await response.json();
    alert(`Task submitted: ${data.task_id}`);
};
