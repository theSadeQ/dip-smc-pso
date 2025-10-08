# Example from: docs\session-continuity.md
# Index: 10
# Runnable: True
# Hash: 3f3e09ea

from session_manager import mark_token_limit_approaching, finalize_session

# Mark approaching limit
mark_token_limit_approaching()

# Finalize with summary
finalize_session("Completed feature X implementation")