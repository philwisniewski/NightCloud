# NightCloud 🌙☁️
**NightCloud** is a resource-sharing platform that turns underutilized personal devices into a distributed cloud infrastructure. This system allows users to contribute their idle devices (overnight or during downtime) to run containerized workloads securely while enabling others to use compute resources in a community-driven cloud environment.

---

## 📑 Features
- **Containerized Task Execution**: Secure task execution using containerization (Podman/Docker) for resource isolation.
- **Web Dashboard**: A simple interface to manage, monitor, and retrieve task outputs.
- **Client Contribution**: CLI tool for contributors to share their device's resources.
- **Task Output Retrieval**: Automatically captures output (e.g., logs, files) and saves them for requesters.

---

## 🛠️ Technology Stack
### Backend:
- **Framework**: Python (Flask)
- **Database**: SQLite (for managing tasks)
- **APIs**: RESTful APIs for task submission and result retrieval

### Frontend:
- **UI**: HTML, CSS, JavaScript
- **Behavior**: Built with Vanilla JS

### Contributor Client:
- **Language**: Python
- **Containerization**: Designed for Podman

### Task Isolation:
- **Containers**: Podman

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
- **Backend Requirements**:
  - Python 3.8+ installed
  - Pipenv or virtualenv for dependency management
- **Frontend Requirements**:
  - Any modern browser (e.g., Chrome, Firefox)
- **Contributor Requirements**:
  - Podman (recommended) or Docker installed locally.

---

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/philwisniewski/NightCloud.git
cd NightCloud

### 3️⃣ Running
- **Start Backend**
  ```bash
  cd backend
  python app.py # runs on port 5000
- **Start Frontend**
  ```bash
  cd frontend
  python -m http.server 8000
- **Start worker**
  ```bash
  cd client
  python client.py
- **Submit tasks**
  - go to http://127.0.0.1:8000
  - fill out form and click submit
