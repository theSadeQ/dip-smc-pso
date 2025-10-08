# Example from: docs\workflows\complete_integration_guide.md
# Index: 20
# Runnable: False
# Hash: c2888158

# example-metadata:
# runnable: false

# Comprehensive integration testing
from src.testing import IntegrationTestSuite

class ComprehensiveIntegrationTests:
    """Complete integration test suite."""

    def __init__(self):
        self.test_suite = IntegrationTestSuite()

    def run_complete_integration_tests(self):
        """Run all integration tests."""

        test_categories = [
            'controller_factory_integration',
            'pso_optimization_integration',
            'simulation_engine_integration',
            'safety_system_integration',
            'monitoring_system_integration',
            'configuration_system_integration'
        ]

        results = {}
        for category in test_categories:
            print(f"🧪 Running {category}...")
            results[category] = self.test_suite.run_test_category(category)

        # Generate integration test report
        self.test_suite.generate_integration_report(results)

        return results

    def test_controller_interoperability(self):
        """Test that all controllers work with all system components."""

        controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']
        components = ['simulation_engine', 'pso_optimizer', 'monitoring_system', 'safety_system']

        compatibility_matrix = {}

        for controller in controllers:
            compatibility_matrix[controller] = {}
            for component in components:
                try:
                    result = self.test_suite.test_component_compatibility(controller, component)
                    compatibility_matrix[controller][component] = result.passed
                except Exception as e:
                    compatibility_matrix[controller][component] = False

        return compatibility_matrix