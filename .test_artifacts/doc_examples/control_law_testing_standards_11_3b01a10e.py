# Example from: docs\control_law_testing_standards.md
# Index: 11
# Runnable: False
# Hash: 3b01a10e

# example-metadata:
# runnable: false

class FactoryConfigurationTestSuite:
    """Test suite for factory and configuration verification."""

    def test_controller_factory_consistency(self) -> FactoryConsistencyTestResult:
        """Test controller factory consistency and correctness."""

        factory_test_cases = []

        # Test all supported controller types
        for controller_type in SUPPORTED_CONTROLLER_TYPES:
            # Test factory creation
            factory_result = self._test_factory_creation(controller_type)

            # Verify controller properties
            property_verification = self._verify_controller_properties(
                factory_result.controller, controller_type
            )

            # Test configuration consistency
            config_consistency = self._test_configuration_consistency(
                factory_result.controller, factory_result.configuration
            )

            factory_test_cases.append(FactoryTestCase(
                controller_type=controller_type,
                factory_result=factory_result,
                property_verification=property_verification,
                config_consistency=config_consistency,
                factory_creation_successful=factory_result.successful and property_verification.valid
            ))

        return FactoryConsistencyTestResult(
            test_cases=factory_test_cases,
            all_factory_creations_successful=all(tc.factory_creation_successful for tc in factory_test_cases),
            factory_issues=self._identify_factory_issues(factory_test_cases)
        )

    def test_configuration_validation(self) -> ConfigurationValidationTestResult:
        """Test configuration validation and error handling."""

        # Test valid configurations
        valid_config_results = self._test_valid_configurations()

        # Test invalid configurations
        invalid_config_results = self._test_invalid_configurations()

        # Test edge case configurations
        edge_case_config_results = self._test_edge_case_configurations()

        return ConfigurationValidationTestResult(
            valid_config_results=valid_config_results,
            invalid_config_results=invalid_config_results,
            edge_case_results=edge_case_config_results,
            configuration_validation_working=self._assess_configuration_validation(
                valid_config_results, invalid_config_results, edge_case_config_results
            )
        )