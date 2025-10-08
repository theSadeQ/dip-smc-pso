# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 9
# Runnable: True
# Hash: 2596c93f

self._mode: Mode  # "swing" or "stabilize"
self._switch_time: Optional[float]  # Time of last handoff
self._stab_state_vars: Tuple  # Stabilizer internal state
self._stab_history: Dict  # Stabilizer history