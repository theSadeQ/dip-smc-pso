# Example from: docs\guides\workflows\hil-workflow.md
# Index: 4
# Runnable: True
# Hash: e6ac5102

# simulate.py now sets PYTHONPATH for client subprocess
client_env = os.environ.copy()
client_env["PYTHONPATH"] = str(REPO_ROOT)
client_proc = subprocess.Popen(client_cmd, cwd=str(REPO_ROOT), env=client_env)