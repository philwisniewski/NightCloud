# backend/app.py

from flask import Flask, redirect, url_for, session, request, jsonify, send_file
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from models import (
    initialize_db, save_task, get_task, get_tasks_for_user, get_or_create_user, user_owns_task, update_task_status
)
import os

import config # secrets


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:8000", "http://localhost:8000"],
)

oauth = OAuth(app)

oauth.register(
    name='auth0',
    client_id=config.AUTH0_CLIENT_ID,
    client_secret=config.AUTH0_CLIENT_SECRET,
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration'
  )

initialize_db()

UPLOAD_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return 'Backend up! Visit /login to authenticate.'


@app.route("/login")
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.auth0.authorize_redirect(redirect_uri)


@app.route("/auth")
def auth():
    token = oauth.auth0.authorize_access_token()
    userinfo = token['userinfo'] if 'userinfo' in token else oauth.auth0.parse_id_token(token)
    user = get_or_create_user(userinfo['sub'], userinfo.get('name'))
    session['user'] = {'id': user['id'], 'sub': userinfo['sub'], 'name': userinfo.get('name')}
    # changed from '/'
    return redirect('http://127.0.0.1:8000')


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/submit-task", methods=["POST"])
def submit_task():
    if 'user' not in session:
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    docker_image = data.get("docker_image")
    command = data.get("command")
    user_id = session['user']['id']
    task_id = save_task(docker_image, command, user_id)
    return jsonify({"task_id": task_id, "status": "Task submitted"})


@app.route('/list-tasks')
def list_tasks():
    if 'user' not in session:
        return jsonify([])
    user_id = session['user']['id']
    tasks = get_tasks_for_user(user_id)
    return jsonify(tasks)


@app.route('/download-stdout/<int:task_id>')
def download_stdout(task_id):
    if 'user' not in session:
        return jsonify({"error": "unauthorized"}), 401
    user_id = session['user']['id']
    if not user_owns_task(user_id, task_id):
        return jsonify({"error": "forbidden"}), 403
    path = f"{UPLOAD_FOLDER}/{task_id}_stdout.txt"
    return send_file(path, as_attachment=True)


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


@app.route('/me')
def me():
    if 'user' in session:
        return jsonify({"id": session['user']['id'], "name": session['user'].get('name')})
    return jsonify({"error": "unauthorized"}), 401


if __name__ == "__main__":
    app.run(debug=True)
