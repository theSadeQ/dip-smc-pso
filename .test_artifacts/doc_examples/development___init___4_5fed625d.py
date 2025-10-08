# Example from: docs\reference\utils\development___init__.md
# Index: 4
# Runnable: True
# Hash: 5fed625d

from src.utils.development import NotebookStateManager

# Create state manager
state_mgr = NotebookStateManager()

# Save current workspace
state_mgr.save_state('experiment_checkpoint.pkl')

# Run risky computation
try:
    risky_computation()
except Exception as e:
    # Restore previous state
    state_mgr.restore_state('experiment_checkpoint.pkl')
    print(f"Restored state after error: {e}")

# Check state consistency
if not state_mgr.check_consistency():
    print("Warning: Notebook cells executed out of order")