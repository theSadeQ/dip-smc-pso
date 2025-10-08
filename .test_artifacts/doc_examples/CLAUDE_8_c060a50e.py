# Example from: docs\CLAUDE.md
# Index: 8
# Runnable: True
# Hash: c060a50e

# Claude automatically throughout session:
update_session_context(current_task="Implementing backup system", phase="testing")
add_completed_todo("Create PowerShell script")
add_completed_todo("Write documentation")
add_next_action("User needs to register Task Scheduler")

# As token limit approaches:
mark_token_limit_approaching()
finalize_session("Backup system implementation complete")