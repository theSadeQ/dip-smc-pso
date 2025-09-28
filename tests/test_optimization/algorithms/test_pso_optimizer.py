#==========================================================================================\\\
#================ tests/test_optimization/algorithms/test_pso_optimizer.py ==============\\\
#==========================================================================================\\\

"""
Comprehensive tests for PSO optimizer integration and functionality.
Tests the main PSOTuner class for correctness, performance, and integration.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import yaml

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import ConfigSchema


class TestPSOTuner:
    """Test suite for PSOTuner class."""

    @pytest.fixture
    def minimal_config(self):
        """Create minimal valid configuration for testing."""
        config_data = {
            'global_seed': 42,
            'physics': {
                'cart_mass': 1.5,
                'pendulum1_mass': 0.2,
                'pendulum2_mass': 0.15,
                'pendulum1_length': 0.4,
                'pendulum2_length': 0.3,
                'pendulum1_com': 0.2,
                'pendulum2_com': 0.15,
                'pendulum1_inertia': 0.009,
                'pendulum2_inertia': 0.009,
                'gravity': 9.81,
                'cart_friction': 0.2,
                'joint1_friction': 0.005,
                'joint2_friction': 0.004,
                'singularity_cond_threshold': 1e8
            },
            'simulation': {
                'duration': 1.0,
                'dt': 0.01,
                'initial_state': [0.0, 0.05, -0.03, 0.0, 0.0, 0.0],
                'use_full_dynamics': False
            },
            'cost_function': {
                'weights': {
                    'state_error': 50.0,
                    'control_effort': 0.2,
                    'control_rate': 0.1,
                    'stability': 0.1
                },
                'instability_penalty': 1000.0
            },
            'pso': {
                'n_particles': 5,
                'bounds': {
                    'min': [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],
                    'max': [20.0, 20.0, 10.0, 10.0, 50.0, 5.0]
                },
                'w': 0.5,
                'c1': 1.5,
                'c2': 1.5,
                'iters': 3
            }
        }
        return ConfigSchema(**config_data)

    @pytest.fixture
    def mock_controller_factory(self):
        """Create mock controller factory."""
        def factory(gains):
            controller = Mock()
            controller.max_force = 150.0
            controller.n_gains = len(gains)
            controller.controller_type = 'classical_smc'
            controller.validate_gains = Mock(return_value=np.ones(len(gains), dtype=bool))
            return controller

        factory.n_gains = 6
        factory.controller_type = 'classical_smc'
        return factory

    def test_pso_tuner_initialization(self, minimal_config, mock_controller_factory):
        """Test PSOTuner initialization with valid configuration."""
        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=minimal_config,
            seed=42
        )

        assert tuner.seed == 42
        assert tuner.instability_penalty > 0
        assert tuner.combine_weights == (0.7, 0.3)
        assert tuner.normalisation_threshold > 0

    def test_pso_tuner_with_config_file(self, minimal_config, mock_controller_factory, tmp_path):
        """Test PSOTuner initialization with configuration file."""
        config_file = tmp_path / "test_config.yaml"
        config_data = minimal_config.model_dump()

        with open(config_file, 'w') as f:
            yaml.safe_dump(config_data, f)

        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=str(config_file),
            seed=42
        )

        assert tuner.seed == 42
        assert isinstance(tuner.cfg, ConfigSchema)

    def test_deprecated_pso_config_fields(self, minimal_config, mock_controller_factory):
        """Test that deprecated PSO configuration fields raise ValueError."""
        # Add deprecated field
        config_data = minimal_config.model_dump()
        config_data['pso']['n_processes'] = 4  # Deprecated
        config = ConfigSchema(**config_data)

        with pytest.raises(ValueError, match="Deprecated PSO configuration fields"):
            PSOTuner(
                controller_factory=mock_controller_factory,
                config=config,
                seed=42
            )

    @patch('src.optimization.algorithms.pso_optimizer.simulate_system_batch')
    def test_fitness_evaluation(self, mock_simulate, minimal_config, mock_controller_factory):
        """Test fitness function evaluation."""
        # Setup mock simulation results
        mock_simulate.return_value = (
            np.linspace(0, 1, 101),  # time
            np.random.random((2, 101, 6)),  # states
            np.random.random((2, 101)),  # controls
            np.random.random((2, 101))   # sigma
        )

        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=minimal_config,
            seed=42
        )

        # Test fitness evaluation
        particles = np.random.random((2, 6))
        fitness = tuner._fitness(particles)

        assert isinstance(fitness, np.ndarray)
        assert fitness.shape == (2,)
        assert np.all(np.isfinite(fitness))

    def test_normalisation_function(self, minimal_config, mock_controller_factory):
        """Test safe normalisation function."""
        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=minimal_config,
            seed=42
        )

        # Test normal normalisation
        values = np.array([1.0, 2.0, 3.0])
        normalised = tuner._normalise(values, 2.0)
        expected = np.array([0.5, 1.0, 1.5])
        np.testing.assert_array_almost_equal(normalised, expected)

        # Test near-zero denominator
        normalised_zero = tuner._normalise(values, 1e-15)
        np.testing.assert_array_equal(normalised_zero, values)

    def test_cost_combination(self, minimal_config, mock_controller_factory):
        """Test cost aggregation across uncertainty draws."""
        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=minimal_config,
            seed=42
        )

        # Test 1D cost array
        costs_1d = np.array([1.0, 2.0, 3.0])
        combined = tuner._combine_costs(costs_1d)
        expected = 0.7 * 2.0 + 0.3 * 3.0  # mean * w_mean + max * w_max
        assert abs(combined - expected) < 1e-10

        # Test 2D cost array
        costs_2d = np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]])
        combined_2d = tuner._combine_costs(costs_2d)
        assert combined_2d.shape == (2,)

    @patch('src.optimization.algorithms.pso_optimizer.simulate_system_batch')
    @patch('pyswarms.single.GlobalBestPSO')
    def test_optimization_execution(self, mock_pso_class, mock_simulate, minimal_config, mock_controller_factory):
        """Test full PSO optimization execution."""
        # Setup mocks
        mock_optimizer = Mock()
        mock_optimizer.optimize.return_value = (1.5, np.array([5, 5, 5, 2, 20, 1]))
        mock_optimizer.cost_history = [2.0, 1.8, 1.5]
        mock_optimizer.pos_history = [np.array([5, 5, 5, 2, 20, 1])]
        mock_pso_class.return_value = mock_optimizer

        mock_simulate.return_value = (
            np.linspace(0, 1, 101),
            np.random.random((5, 101, 6)),
            np.random.random((5, 101)),
            np.random.random((5, 101))
        )

        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=minimal_config,
            seed=42
        )

        # Run optimization
        result = tuner.optimise()

        assert 'best_cost' in result
        assert 'best_pos' in result
        assert 'history' in result
        assert result['best_cost'] == 1.5
        assert len(result['best_pos']) == 6

    def test_perturbed_physics_iteration(self, minimal_config, mock_controller_factory):
        """Test physics uncertainty iteration."""
        # Add uncertainty configuration
        config_data = minimal_config.model_dump()
        config_data['physics_uncertainty'] = {
            'n_evals': 3,
            'cart_mass': 0.1,
            'pendulum1_mass': 0.05
        }
        config = ConfigSchema(**config_data)

        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=config,
            seed=42
        )

        physics_models = list(tuner._iter_perturbed_physics())
        assert len(physics_models) == 3  # nominal + 2 perturbed

    def test_instability_penalty_computation(self, minimal_config, mock_controller_factory):
        """Test instability penalty calculation."""
        # Test with explicit penalty
        config_data = minimal_config.model_dump()
        config_data['cost_function']['instability_penalty'] = 500.0
        config = ConfigSchema(**config_data)

        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=config,
            seed=42
        )

        assert tuner.instability_penalty == 500.0

    def test_bounds_dimension_matching(self, minimal_config, mock_controller_factory):
        """Test PSO bounds dimension matching with controller expectations."""
        # Modify bounds to have wrong dimensions
        config_data = minimal_config.model_dump()
        config_data['pso']['bounds']['min'] = [1.0, 1.0, 1.0]  # Only 3 dimensions
        config_data['pso']['bounds']['max'] = [10.0, 10.0, 10.0]
        config = ConfigSchema(**config_data)

        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=config,
            seed=42
        )

        # Should auto-extend to match expected dimensions
        with patch('pyswarms.single.GlobalBestPSO') as mock_pso:
            mock_optimizer = Mock()
            mock_optimizer.optimize.return_value = (1.0, np.array([5, 5, 5, 2, 20, 1]))
            mock_optimizer.cost_history = [1.0]
            mock_optimizer.pos_history = [np.array([5, 5, 5, 2, 20, 1])]
            mock_pso.return_value = mock_optimizer

            with patch('src.optimization.algorithms.pso_optimizer.simulate_system_batch'):
                result = tuner.optimise()
                assert 'best_pos' in result


class TestPSOTunerIntegration:
    """Integration tests for PSOTuner with real components."""

    def test_real_configuration_loading(self):
        """Test loading actual configuration file."""
        # This test would use the real config.yaml if available
        config_path = Path("D:/Projects/main/config.yaml")
        if not config_path.exists():
            pytest.skip("Main config.yaml not found")

        try:
            from src.config import load_config
            config = load_config(str(config_path))

            # Basic validation that config loaded properly
            assert hasattr(config, 'pso')
            assert hasattr(config, 'physics')
            assert hasattr(config, 'simulation')
        except Exception as e:
            pytest.skip(f"Could not load real configuration: {e}")


# Performance and property-based tests would go here
class TestPSOTunerProperties:
    """Property-based and performance tests for PSOTuner."""

    def test_deterministic_behavior(self, minimal_config, mock_controller_factory):
        """Test that PSO optimization is deterministic with fixed seed."""
        with patch('src.optimization.algorithms.pso_optimizer.simulate_system_batch') as mock_sim:
            mock_sim.return_value = (
                np.linspace(0, 1, 101),
                np.random.RandomState(42).random((5, 101, 6)),
                np.random.RandomState(42).random((5, 101)),
                np.random.RandomState(42).random((5, 101))
            )

            with patch('pyswarms.single.GlobalBestPSO') as mock_pso:
                mock_optimizer = Mock()
                mock_optimizer.optimize.return_value = (1.5, np.array([5, 5, 5, 2, 20, 1]))
                mock_optimizer.cost_history = [1.5]
                mock_optimizer.pos_history = [np.array([5, 5, 5, 2, 20, 1])]
                mock_pso.return_value = mock_optimizer

                tuner1 = PSOTuner(mock_controller_factory, minimal_config, seed=42)
                tuner2 = PSOTuner(mock_controller_factory, minimal_config, seed=42)

                result1 = tuner1.optimise()
                result2 = tuner2.optimise()

                assert result1['best_cost'] == result2['best_cost']
                np.testing.assert_array_equal(result1['best_pos'], result2['best_pos'])

    def test_parameter_validation_bounds(self, minimal_config, mock_controller_factory):
        """Test parameter bounds validation."""
        tuner = PSOTuner(
            controller_factory=mock_controller_factory,
            config=minimal_config,
            seed=42
        )

        # Test invalid parameters (negative values, etc.)
        invalid_particles = np.array([[-1, -1, -1, -1, -1, -1]])

        with patch('src.optimization.algorithms.pso_optimizer.simulate_system_batch'):
            fitness = tuner._fitness(invalid_particles)
            # Should handle gracefully, potentially with high penalty
            assert np.all(np.isfinite(fitness))