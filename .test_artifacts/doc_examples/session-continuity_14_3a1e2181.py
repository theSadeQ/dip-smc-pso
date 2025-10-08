# Example from: docs\session-continuity.md
# Index: 14
# Runnable: True
# Hash: 3a1e2181

state = load_session()
session_count = state['metadata']['session_count']
print(f"This is session #{session_count}")