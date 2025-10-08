# Example from: docs\api\phase_4_2_completion_report.md
# Index: 5
# Runnable: True
# Hash: 33e79149

# tests/test_factory_examples.py

import pytest
import numpy as np
from src.controllers.factory import create_controller, list_available_controllers
from src.config import load_config

class TestFactoryExamples:
    """Validate all documented code examples."""

    @pytest.fixture
    def config(self):
        """Load configuration for tests."""
        return load_config("config.yaml")

    def test_example_1_basic_usage(self, config):
        """Test Example 1: Basic Factory Usage."""
        # Example code from docs
        controller = create_controller('classical_smc', config)
        assert controller is not None
        assert len(controller.gains) == 6

        state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])
        result = controller.compute_control(state, 0.0, {})
        assert result is not None

    def test_example_2_pso_optimized(self, config):
        """Test Example 2: PSO-Optimized Controller Creation."""
        optimized_gains = [25.3, 18.7, 14.2, 10.8, 42.6, 6.1]
        controller = create_controller('classical_smc', config, gains=optimized_gains)
        assert controller.gains == optimized_gains

    def test_example_3_batch_comparison(self, config):
        """Test Example 3: Batch Controller Comparison."""
        controllers = {}
        for controller_type in list_available_controllers():
            controller = create_controller(controller_type, config)
            controllers[controller_type] = controller

        assert len(controllers) >= 4  # At least 4 SMC types

    def test_example_4_custom_override(self, config):
        """Test Example 4: Custom Configuration Override."""
        custom_gains = [35.0, 25.0, 18.0, 14.0, 50.0, 8.0]
        controller = create_controller('classical_smc', config, gains=custom_gains)
        assert controller.gains == custom_gains

    def test_example_5_error_handling(self, config):
        """Test Example 5: Error Handling and Validation."""
        # Valid creation
        controller = create_controller('classical_smc', config)
        assert controller is not None

        # Invalid controller type
        with pytest.raises(ValueError, match="Unknown controller type"):
            create_controller('nonexistent_controller', config)

        # Invalid gain count
        with pytest.raises(ValueError, match="requires 6 gains"):
            create_controller('classical_smc', config, gains=[10.0, 20.0])

        # STA constraint violation
        with pytest.raises(ValueError, match="K1 > K2"):
            create_controller('sta_smc', config, gains=[15.0, 20.0, 12.0, 8.0, 6.0, 4.0])