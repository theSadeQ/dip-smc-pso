# Example from: docs\architecture\controller_system_architecture.md
# Index: 11
# Runnable: False
# Hash: e3491295

class GracefulDegradationManager:
    """Manage system degradation under error conditions."""

    @staticmethod
    def handle_controller_failure(
        failed_controller: str,
        available_controllers: List[str]
    ) -> DegradationStrategy:
        """Determine graceful degradation strategy."""

        # Preference order for fallback controllers
        fallback_preferences = {
            'hybrid_adaptive_sta_smc': ['sta_smc', 'adaptive_smc', 'classical_smc'],
            'sta_smc': ['classical_smc', 'adaptive_smc'],
            'adaptive_smc': ['classical_smc', 'sta_smc'],
            'classical_smc': ['adaptive_smc', 'sta_smc']
        }

        preferences = fallback_preferences.get(failed_controller, [])

        for fallback in preferences:
            if fallback in available_controllers:
                return DegradationStrategy(
                    fallback_controller=fallback,
                    degradation_level='graceful',
                    performance_impact='minimal'
                )

        # No suitable fallback available
        return DegradationStrategy(
            fallback_controller=None,
            degradation_level='critical',
            performance_impact='severe'
        )