# Example from: docs\CLAUDE.md
# Index: 7
# Runnable: False
# Hash: a8271ac2

# Check for continuable session
has_recent_session(threshold_hours=24) -> bool

# Load session state
load_session() -> Optional[Dict]

# Get human-readable summary
get_session_summary() -> str

# Update session context
update_session_context(**kwargs) -> bool

# Track progress
add_completed_todo(todo: str) -> bool
add_decision(decision: str) -> bool
add_next_action(action: str) -> bool

# Prepare for handoff
mark_token_limit_approaching() -> bool
finalize_session(summary: str) -> bool