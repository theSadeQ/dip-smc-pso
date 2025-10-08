# Example from: docs\issue_12_continuation_prompt.md
# Index: 2
# Runnable: True
# Hash: 94d6ac9d

# Update controller_defaults (factory fallback)
  updated_default = default_ctrl_config.model_copy(update={'gains': gains.tolist()})
  setattr(temp_config.controller_defaults, controller_type, updated_default)

  # Update controllers (primary source)
  updated_ctrl = ctrl_config.model_copy(update={'gains': gains.tolist()})
  setattr(temp_config.controllers, controller_type, updated_ctrl)