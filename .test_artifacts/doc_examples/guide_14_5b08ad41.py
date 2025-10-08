# Example from: docs\optimization_simulation\guide.md
# Index: 14
# Runnable: True
# Hash: 5b08ad41

@model_validator(mode="after")
def _duration_at_least_dt(self):
    if self.duration < self.dt:
        raise ValueError("duration must be >= dt (temporal consistency)")
    return self