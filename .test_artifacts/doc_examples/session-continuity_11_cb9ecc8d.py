# Example from: docs\session-continuity.md
# Index: 11
# Runnable: True
# Hash: cb9ecc8d

# Claude automatically throughout:
update_session_context(current_task="Add logging module", phase="implementation")
add_completed_todo("Create logger.py")
add_completed_todo("Add log configuration")
add_decision("Use Python logging library")
add_next_action("Write unit tests for logger")

# Token limit approaching:
finalize_session("Logging module implementation complete")