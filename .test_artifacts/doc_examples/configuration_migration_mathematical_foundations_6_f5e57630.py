# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 6
# Runnable: False
# Hash: f5e57630

# example-metadata:
# runnable: false

class PerformanceAnalyzer:
    """Analyze performance preservation during migration."""

    @staticmethod
    def analyze_control_bandwidth(old_gains: List[float], new_gains: List[float], controller_type: str) -> Dict[str, Any]:
        """Analyze control bandwidth preservation."""

        if controller_type == 'classical_smc':
            if len(old_gains) >= 4 and len(new_gains) >= 4:
                old_bandwidth = min(old_gains[2], old_gains[3])  # min(λ1, λ2)
                new_bandwidth = min(new_gains[2], new_gains[3])

                bandwidth_ratio = new_bandwidth / old_bandwidth

                return {
                    'old_bandwidth': old_bandwidth,
                    'new_bandwidth': new_bandwidth,
                    'bandwidth_ratio': bandwidth_ratio,
                    'performance_preserved': 0.8 <= bandwidth_ratio <= 1.2  # ±20% tolerance
                }

        elif controller_type == 'adaptive_smc':
            if len(old_gains) >= 4 and len(new_gains) >= 4:
                old_adaptation_rate = old_gains[4] if len(old_gains) > 4 else 1.0
                new_adaptation_rate = new_gains[4] if len(new_gains) > 4 else 1.0

                adaptation_ratio = new_adaptation_rate / old_adaptation_rate

                return {
                    'old_adaptation_rate': old_adaptation_rate,
                    'new_adaptation_rate': new_adaptation_rate,
                    'adaptation_ratio': adaptation_ratio,
                    'performance_preserved': 0.5 <= adaptation_ratio <= 2.0  # ±100% tolerance
                }

        return {'analysis': 'not_applicable', 'controller_type': controller_type}

    @staticmethod
    def estimate_settling_time_change(old_config: Dict[str, Any], new_config: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate settling time changes after migration."""

        old_gains = old_config.get('gains', [])
        new_gains = new_config.get('gains', [])

        if len(old_gains) >= 4 and len(new_gains) >= 4:
            # Simplified settling time estimate based on surface coefficients
            old_settling = 4.0 / min(old_gains[2], old_gains[3])  # 4/min(λ1, λ2)
            new_settling = 4.0 / min(new_gains[2], new_gains[3])

            settling_ratio = new_settling / old_settling

            return {
                'old_settling_time': old_settling,
                'new_settling_time': new_settling,
                'settling_ratio': settling_ratio,
                'performance_change': 'improved' if settling_ratio < 1.0 else 'degraded' if settling_ratio > 1.1 else 'maintained'
            }

        return {'analysis': 'insufficient_data'}

# Performance analysis example
old_config = {'gains': [20, 15, 12, 8, 35]}
new_config = {'gains': [20, 15, 12, 8, 35, 5]}

bandwidth_analysis = PerformanceAnalyzer.analyze_control_bandwidth(
    old_config['gains'], new_config['gains'], 'classical_smc'
)
print("Bandwidth analysis:", bandwidth_analysis)

settling_analysis = PerformanceAnalyzer.estimate_settling_time_change(old_config, new_config)
print("Settling time analysis:", settling_analysis)