# Example from: docs\factory\factory_integration_user_guide.md
# Index: 1
# Runnable: True
# Hash: abd8cb80

from src.controllers.factory import create_controller

# Classical SMC with enhanced validation
controller = create_controller(
    controller_type='classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]  # All 6 gains required
)

# Super-Twisting SMC with automatic parameter handling
sta_controller = create_controller(
    controller_type='sta_smc',
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0]  # K1, K2, k1, k2, λ1, λ2
)

# Adaptive SMC with gamma included in gains
adaptive_controller = create_controller(
    controller_type='adaptive_smc',
    gains=[25.0, 18.0, 15.0, 10.0, 4.0]  # k1, k2, λ1, λ2, γ
)