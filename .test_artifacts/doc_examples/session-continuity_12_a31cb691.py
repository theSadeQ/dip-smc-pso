# Example from: docs\session-continuity.md
# Index: 12
# Runnable: True
# Hash: a31cb691

update_session_context(
    current_task="PSO optimization for classical SMC",
    phase="running"
)
add_decision("PSO parameters: 30 particles, 150 iterations")
add_next_action("Wait for PSO completion (~3 hours)")
add_next_action("Validate results when complete")
finalize_session("PSO optimization started, awaiting completion")