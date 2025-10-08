# Example from: docs\workflows\complete_integration_guide.md
# Index: 13
# Runnable: True
# Hash: 0d1841db

# Adaptive controller selection based on performance
from src.utils.adaptive_selection import ControllerSelector

class AdaptiveControllerSystem:
    """System that adaptively selects best controller."""

    def __init__(self):
        self.controllers = {
            'classical_smc': create_controller('classical_smc'),
            'adaptive_smc': create_controller('adaptive_smc'),
            'sta_smc': create_controller('sta_smc'),
            'hybrid_adaptive_sta_smc': create_controller('hybrid_adaptive_sta_smc')
        }

        self.selector = ControllerSelector(
            performance_window=100,  # Evaluate over 100 samples
            switching_threshold=0.1,  # 10% performance improvement
            switching_cooldown=50    # Minimum 50 samples between switches
        )

    def adaptive_control_loop(self, duration: float):
        """Run adaptive control with automatic controller selection."""

        current_controller = 'hybrid_adaptive_sta_smc'  # Start with best
        performance_history = []

        for t in simulation_time_steps(duration):
            state = get_system_state()

            # Compute control with current controller
            control = self.controllers[current_controller].compute_control(state)

            # Apply control
            apply_control(control)

            # Monitor performance
            performance = self.selector.evaluate_performance(state, control)
            performance_history.append(performance)

            # Check if controller switch needed
            if self.selector.should_switch(performance_history):
                new_controller = self.selector.select_best_controller(
                    self.controllers,
                    current_state=state,
                    performance_history=performance_history
                )

                if new_controller != current_controller:
                    print(f"🔄 Switching from {current_controller} to {new_controller}")
                    current_controller = new_controller

        return performance_history