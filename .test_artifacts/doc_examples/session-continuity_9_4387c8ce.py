# Example from: docs\session-continuity.md
# Index: 9
# Runnable: True
# Hash: 4387c8ce

from session_manager import add_completed_todo, add_decision, add_next_action

# Mark todo as complete
add_completed_todo("Write unit tests")

# Record important decision
add_decision("Use pytest for testing framework")

# Specify next action
add_next_action("Run full test suite")