# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 4
# Runnable: True
# Hash: e6078fdc

if dynamics_model is not None:
    self._dynamics_ref = weakref.ref(dynamics_model)
else:
    self._dynamics_ref = lambda: None