# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 1
# Runnable: False
# Hash: 9f3c3a04

# BEFORE (35 occurrences across 3 files)
return self._create_failure_result(
    "Invalid inputs",
    state=state.copy(),           # ❌ Unnecessary
    control_input=control_input.copy(),  # ❌ Unnecessary
    time=time
)

# AFTER
return self._create_failure_result(
    "Invalid inputs",
    state=state,                  # ✅ No mutation after return
    control_input=control_input,  # ✅ Caller owns arrays
    time=time
)