import os
import platform
import subprocess
import time

# 👉 YOUR PROJECT PATH
PROJECT_PATH = "/Volumes/Niladittya/codex/fliqzworld/ai/virtual-ai-creator"

# 👉 Your venv python (IMPORTANT)
PYTHON_PATH = f"{PROJECT_PATH}/.venv/bin/python"

commands = [
    f"{PYTHON_PATH} -m workers.run_activity_worker",
    f"{PYTHON_PATH} -m workers.message_worker",
    f"{PYTHON_PATH} -m workers.importance_worker",
    f"{PYTHON_PATH} -m workers.memory_processor_worker",
    f"{PYTHON_PATH} -m workers.db_worker"
]

system = platform.system()

print(f"🚀 Launching workers on {system}...\n")

for cmd in commands:
    try:
        if system == "Darwin":  # macOS
            subprocess.Popen([
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "cd {PROJECT_PATH} && {cmd}"'
            ])

        elif system == "Windows":
            subprocess.Popen(
                ["cmd", "/c", "start", "cmd", "/k", f"cd /d {PROJECT_PATH} && {cmd}"],
                shell=True
            )

        elif system == "Linux":
            subprocess.Popen([
                "gnome-terminal",
                "--",
                "bash",
                "-c",
                f"cd {PROJECT_PATH} && {cmd}; exec bash"
            ])

        time.sleep(0.5)

    except Exception as e:
        print(f"❌ Failed to launch {cmd}: {e}")