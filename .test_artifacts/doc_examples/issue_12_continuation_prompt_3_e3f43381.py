# Example from: docs\issue_12_continuation_prompt.md
# Index: 3
# Runnable: True
# Hash: e3f43381

# WRONG - Silent failure (Pydantic models are frozen)
setattr(config.controllers.classical_smc, 'gains', new_gains)

# CORRECT - Creates new immutable object
updated = config.controllers.classical_smc.model_copy(update={'gains': new_gains})
setattr(config.controllers, 'classical_smc', updated)