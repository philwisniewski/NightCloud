#!/bin/bash

set -euo pipefail

REPO_URL="$1"
TASK_ID="$2"
SERVER_URL="http://127.0.0.1:5000"
VM_NAME="task-$TASK_ID"
MAX_RUNTIME=7200

# spin up Lima VM
limactl start lima.yml --name "$VM_NAME"

# run job and capture output
OUTPUT=$(lima shell "$VM_NAME" bash <<EOF
set -e
git clone "$REPO_URL" repo
cd repo
docker build -t task .
docker run --rm \
  --cap-drop=ALL \
  --security-opt no-new-privileges \
  --read-only \
  --pids-limit=64
  --memory=512m \
  task
EOF
)

# send output back to server
curl -X POST "$SERVER_URL/upload-results" \
  -F task_id="$TASK_ID" \
  -F stdout="$OUTPUT"

# destroy VM
limactl stop "$VM_NAME"
limactl delete "$VM_NAME"
