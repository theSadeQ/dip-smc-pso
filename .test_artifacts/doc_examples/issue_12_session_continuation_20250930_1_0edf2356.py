# Example from: docs\issue_12_session_continuation_20250930.md
# Index: 1
# Runnable: True
# Hash: 0edf2356

# Current fitness (optimize_chattering_direct.py):
chattering_penalty = max(0, chattering_index - 2.0) * 10.0
# ↑ This is ZERO when chattering < 2.0!

fitness = tracking_error_rms + chattering_penalty + tracking_penalty + effort_penalty
# ↑ Dominated by tracking_error_rms