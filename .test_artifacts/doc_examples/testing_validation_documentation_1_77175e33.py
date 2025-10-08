# Example from: docs\factory\testing_validation_documentation.md
# Index: 1
# Runnable: True
# Hash: 77175e33

import pytest
import numpy as np
from unittest.mock import Mock, patch
from typing import Dict, Any, List

from src.controllers.factory import (
    create_controller, SMCFactory, SMCType, SMCConfig,
    _resolve_controller_gains, _validate_controller_gains,
    _extract_controller_parameters, CONTROLLER_REGISTRY
)

class TestControllerFactoryCore:
    """Core factory functionality testing."""

    def setup_method(self):
        """Setup test fixtures for each test method."""
        self.plant_config = self._create_test_plant_config()
        self.valid_gain_sets = {
            'classical_smc': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
            'adaptive_smc': [25.0, 18.0, 15.0, 10.0, 4.0],
            'sta_smc': [35.0, 20.0, 25.0, 18.0, 12.0, 8.0],
            'hybrid_adaptive_sta_smc': [18.0, 12.0, 10.0, 8.0]
        }

    def _create_test_plant_config(self) -> Any:
        """Create standardized test plant configuration."""
        from src.plant.configurations import ConfigurationFactory
        return ConfigurationFactory.create_default_config("simplified")

    @pytest.mark.parametrize("controller_type,expected_gains", [
        ('classical_smc', 6),
        ('adaptive_smc', 5),
        ('sta_smc', 6),
        ('hybrid_adaptive_sta_smc', 4)
    ])
    def test_controller_creation_success(self, controller_type: str, expected_gains: int):
        """Test successful controller creation for all types."""
        gains = self.valid_gain_sets[controller_type]

        controller = create_controller(
            controller_type=controller_type,
            config=self.plant_config,
            gains=gains
        )

        assert controller is not None
        assert hasattr(controller, 'compute_control')
        assert hasattr(controller, 'gains')
        assert len(controller.gains) == expected_gains

    def test_controller_registry_completeness(self):
        """Test that controller registry is complete and well-formed."""
        required_keys = [
            'class', 'config_class', 'default_gains',
            'gain_count', 'description', 'supports_dynamics', 'required_params'
        ]

        for controller_type, info in CONTROLLER_REGISTRY.items():
            for key in required_keys:
                assert key in info, f"Missing key '{key}' in registry for {controller_type}"

            # Validate default gains structure
            assert len(info['default_gains']) == info['gain_count']
            assert all(isinstance(g, (int, float)) for g in info['default_gains'])
            assert all(g > 0 for g in info['default_gains'])

    def test_parameter_resolution_hierarchy(self):
        """Test parameter resolution follows correct hierarchy."""
        controller_type = 'classical_smc'
        controller_info = CONTROLLER_REGISTRY[controller_type]

        # Test 1: Explicit gains take priority
        explicit_gains = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        resolved_gains = _resolve_controller_gains(
            gains=explicit_gains,
            config=None,
            controller_type=controller_type,
            controller_info=controller_info
        )
        assert resolved_gains == explicit_gains

        # Test 2: Config gains when no explicit gains
        config_mock = Mock()
        config_mock.controllers = {
            controller_type: {'gains': [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]}
        }
        resolved_gains = _resolve_controller_gains(
            gains=None,
            config=config_mock,
            controller_type=controller_type,
            controller_info=controller_info
        )
        assert resolved_gains == [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]

        # Test 3: Default gains as fallback
        resolved_gains = _resolve_controller_gains(
            gains=None,
            config=None,
            controller_type=controller_type,
            controller_info=controller_info
        )
        assert resolved_gains == controller_info['default_gains']

    @pytest.mark.parametrize("invalid_gains,expected_error", [
        ([], ValueError),  # Empty gains
        ([1.0, 2.0], ValueError),  # Too few gains
        ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], ValueError),  # Too many gains
        ([np.nan, 2.0, 3.0, 4.0, 5.0, 6.0], ValueError),  # NaN gain
        ([np.inf, 2.0, 3.0, 4.0, 5.0, 6.0], ValueError),  # Infinite gain
        ([-1.0, 2.0, 3.0, 4.0, 5.0, 6.0], ValueError),  # Negative gain
        ([0.0, 2.0, 3.0, 4.0, 5.0, 6.0], ValueError),  # Zero gain
        (['a', 2.0, 3.0, 4.0, 5.0, 6.0], ValueError),  # Non-numeric gain
    ])
    def test_gain_validation_errors(self, invalid_gains: List, expected_error: type):
        """Test gain validation properly catches invalid inputs."""
        controller_info = CONTROLLER_REGISTRY['classical_smc']

        with pytest.raises(expected_error):
            _validate_controller_gains(invalid_gains, controller_info)

    def test_configuration_parameter_extraction(self):
        """Test configuration parameter extraction from various formats."""
        # Test with Pydantic-like config
        pydantic_config = Mock()
        pydantic_config.controllers = {
            'classical_smc': Mock()
        }
        pydantic_config.controllers['classical_smc'].model_dump.return_value = {
            'gains': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            'max_force': 100.0,
            'boundary_layer': 0.02
        }

        params = _extract_controller_parameters(
            pydantic_config, 'classical_smc', CONTROLLER_REGISTRY['classical_smc']
        )

        assert 'gains' in params
        assert 'max_force' in params
        assert 'boundary_layer' in params

        # Test with dictionary config
        dict_config = Mock()
        dict_config.controllers = {
            'classical_smc': {
                'gains': [7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
                'max_force': 150.0
            }
        }

        params = _extract_controller_parameters(
            dict_config, 'classical_smc', CONTROLLER_REGISTRY['classical_smc']
        )

        assert params['gains'] == [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        assert params['max_force'] == 150.0

    def test_thread_safety_basic(self):
        """Test basic thread safety of factory operations."""
        import threading
        import time

        results = []
        errors = []

        def create_controller_threaded(thread_id: int):
            try:
                for i in range(5):
                    gains = [10.0 + thread_id, 5.0, 8.0, 3.0, 15.0, 2.0]
                    controller = create_controller(
                        'classical_smc',
                        self.plant_config,
                        gains
                    )
                    assert controller is not None
                    time.sleep(0.001)  # Small delay to increase contention
                results.append(True)
            except Exception as e:
                errors.append(f"Thread {thread_id}: {str(e)}")
                results.append(False)

        # Create and run multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=create_controller_threaded, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify results
        assert not errors, f"Thread safety errors: {errors}"
        assert all(results), "Some threads failed"

    def test_error_recovery_mechanisms(self):
        """Test error recovery and graceful degradation."""
        # Test with invalid config that should trigger fallback
        invalid_config = Mock()
        invalid_config.controllers = None  # This should cause extraction to fail

        # Should still create controller using default parameters
        controller = create_controller(
            'classical_smc',
            invalid_config,
            [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
        )

        assert controller is not None

    def test_memory_usage_validation(self):
        """Test that factory doesn't leak memory during intensive use."""
        import gc
        import weakref

        # Create many controllers and track weak references
        weak_refs = []

        for i in range(20):
            gains = [10.0 + i, 5.0, 8.0, 3.0, 15.0, 2.0]
            controller = create_controller(
                'classical_smc',
                self.plant_config,
                gains
            )
            weak_refs.append(weakref.ref(controller))
            del controller

        # Force garbage collection
        gc.collect()

        # Check that controllers were properly cleaned up
        alive_refs = [ref for ref in weak_refs if ref() is not None]
        assert len(alive_refs) <= 3, f"Memory leak detected: {len(alive_refs)} controllers still alive"