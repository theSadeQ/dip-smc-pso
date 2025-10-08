# Example from: docs\session-continuity.md
# Index: 7
# Runnable: True
# Hash: ce96d1a1

from session_manager import load_session

state = load_session()
if state:
    current_task = state['context']['current_task']
    phase = state['context']['phase']
    next_actions = state['next_actions']