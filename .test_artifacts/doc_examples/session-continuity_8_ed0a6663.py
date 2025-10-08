# Example from: docs\session-continuity.md
# Index: 8
# Runnable: True
# Hash: ed0a6663

from session_manager import update_session_context

update_session_context(
    current_task="Implementing feature X",
    phase="testing",
    last_commit="abc1234"
)