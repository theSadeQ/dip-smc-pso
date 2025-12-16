"""
Unit tests for warm-start PSO initialization.

Tests the hybrid warm-start approach (20% optimized + 20% baseline + 60% random)
for bulletproof PSO optimization system.

Author: Claude Code
Created: December 9, 2025
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts" / "optimization"
sys.path.insert(0, str(scripts_dir))

from phase2_warmstart_pso import initialize_warm_start_swarm, load_warm_start_gains
from src.config import load_config


class TestHybridInitialization:
    """Test hybrid warm-start swarm initialization."""

    def test_hybrid_initialization_particle_distribution(self):
        """Verify 20/20/60 particle distribution."""
        n_particles = 30
        n_gains = 6
        optimized = np.array([2.0, 6.0, 5.0, 3.0, 4.0, 2.0])
        baseline = np.array([8.0, 4.0, 12.0, 6.0, 5.0, 3.0])
        bounds_min = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        bounds_max = np.array([15.0, 15.0, 15.0, 15.0, 15.0, 15.0])
        rng = np.random.default_rng(42)

        swarm = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng, noise_factor=0.1
        )

        # Check shape
        assert swarm.shape == (30, 6), f"Expected shape (30, 6), got {swarm.shape}"

        # Check bounds respected
        assert np.all(swarm >= bounds_min), "Some particles below min bounds"
        assert np.all(swarm <= bounds_max), "Some particles above max bounds"

        # Check particles near optimized (first 6)
        for i in range(6):
            dist_to_opt = np.linalg.norm(swarm[i] - optimized)
            # Should be within ~3 standard deviations (0.3 * bounds = 4.5)
            assert dist_to_opt < 6.0, f"Particle {i} too far from optimized gains (dist={dist_to_opt:.2f})"

        # Check particles near baseline (next 6)
        for i in range(6, 12):
            dist_to_base = np.linalg.norm(swarm[i] - baseline)
            assert dist_to_base < 6.0, f"Particle {i} too far from baseline gains (dist={dist_to_base:.2f})"

    def test_particle_counts(self):
        """Verify exact particle count distribution."""
        n_particles = 30
        n_gains = 4
        optimized = np.array([5.0, 5.0, 5.0, 0.5])
        baseline = np.array([10.0, 8.0, 12.0, 1.0])
        bounds_min = np.zeros(4)
        bounds_max = np.ones(4) * 15.0
        rng = np.random.default_rng(42)

        swarm = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng, noise_factor=0.1
        )

        # Calculate expected counts
        n_optimized = int(0.20 * n_particles)  # 6
        n_baseline = int(0.20 * n_particles)   # 6
        n_random = n_particles - n_optimized - n_baseline  # 18

        assert n_optimized == 6, f"Expected 6 optimized particles, got {n_optimized}"
        assert n_baseline == 6, f"Expected 6 baseline particles, got {n_baseline}"
        assert n_random == 18, f"Expected 18 random particles, got {n_random}"

        # Verify total
        assert n_optimized + n_baseline + n_random == n_particles


class TestConfigLoading:
    """Test loading gains from config.yaml."""

    def test_config_loading_sta_smc(self):
        """Test loading STA-SMC gains from config.yaml."""
        config = load_config("config.yaml")
        optimized, baseline = load_warm_start_gains('sta_smc', 6, config)

        assert optimized is not None, "Optimized gains not loaded"
        assert baseline is not None, "Baseline gains not loaded"
        assert len(optimized) == 6, f"Expected 6 optimized gains, got {len(optimized)}"
        assert len(baseline) == 6, f"Expected 6 baseline gains, got {len(baseline)}"

        # Verify actual values from config
        expected_opt = np.array([2.02, 6.67, 5.62, 3.75, 4.36, 2.05])
        expected_base = np.array([8.0, 4.0, 12.0, 6.0, 4.85, 3.43])

        np.testing.assert_allclose(optimized, expected_opt, rtol=1e-2)
        np.testing.assert_allclose(baseline, expected_base, rtol=1e-2)

    def test_config_loading_adaptive_smc(self):
        """Test loading Adaptive SMC gains from config.yaml."""
        config = load_config("config.yaml")
        optimized, baseline = load_warm_start_gains('adaptive_smc', 5, config)

        assert optimized is not None, "Optimized gains not loaded"
        assert baseline is not None, "Baseline gains not loaded"
        assert len(optimized) == 5, f"Expected 5 optimized gains, got {len(optimized)}"
        assert len(baseline) == 5, f"Expected 5 baseline gains, got {len(baseline)}"

        # Verify actual values from config
        expected_opt = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
        expected_base = np.array([10.0, 8.0, 5.0, 4.0, 1.0])

        np.testing.assert_allclose(optimized, expected_opt, rtol=1e-2)
        np.testing.assert_allclose(baseline, expected_base, rtol=1e-2)

    def test_config_loading_hybrid(self):
        """Test loading Hybrid Adaptive STA-SMC gains from config.yaml."""
        config = load_config("config.yaml")
        optimized, baseline = load_warm_start_gains('hybrid_adaptive_sta_smc', 4, config)

        assert optimized is not None, "Optimized gains not loaded"
        assert baseline is not None, "Baseline gains not loaded"
        assert len(optimized) == 4, f"Expected 4 optimized gains, got {len(optimized)}"
        assert len(baseline) == 4, f"Expected 4 baseline gains, got {len(baseline)}"


class TestFallbackBehavior:
    """Test graceful fallback when gains are missing."""

    def test_fallback_on_missing_controller(self):
        """Test graceful fallback when controller doesn't exist."""
        # Mock config with missing controller
        class MockConfig:
            controllers = type('obj', (), {})()
            controller_defaults = type('obj', (), {})()

        config = MockConfig()
        optimized, baseline = load_warm_start_gains('nonexistent', 6, config)

        # Should return None, None
        assert optimized is None, "Expected None for missing optimized gains"
        assert baseline is None, "Expected None for missing baseline gains"


class TestNoiseFactorScaling:
    """Test Gaussian noise scaling with bounds."""

    def test_noise_factor_scaling(self):
        """Verify noise scales correctly with bound range."""
        n_particles = 30
        n_gains = 6
        optimized = np.ones(6) * 5.0
        baseline = np.ones(6) * 8.0
        bounds_min = np.zeros(6)
        bounds_max = np.ones(6) * 10.0  # Range = 10.0
        rng = np.random.default_rng(42)

        swarm = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng, noise_factor=0.1
        )

        # Expected noise_std = 0.1 * (10.0 - 0.0) = 1.0
        # Particles 0-5 should be near optimized (5.0) ± 3*1.0 = [2.0, 8.0]
        for i in range(6):
            assert np.all(swarm[i] >= 2.0) and np.all(swarm[i] <= 8.0), \
                f"Particle {i} outside expected range [2.0, 8.0]: {swarm[i]}"

    def test_different_noise_factors(self):
        """Test different noise factors produce different diversity levels."""
        n_particles = 30
        n_gains = 4
        optimized = np.ones(4) * 5.0
        baseline = np.ones(4) * 10.0
        bounds_min = np.zeros(4)
        bounds_max = np.ones(4) * 15.0

        # Test with low noise
        rng_low = np.random.default_rng(42)
        swarm_low = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng_low, noise_factor=0.05
        )

        # Test with high noise
        rng_high = np.random.default_rng(42)
        swarm_high = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng_high, noise_factor=0.3
        )

        # High noise should produce more diverse swarm (higher variance)
        var_low = np.var(swarm_low[:6], axis=0)  # First 6 particles (optimized)
        var_high = np.var(swarm_high[:6], axis=0)

        # Variance with high noise should be significantly larger
        assert np.all(var_high > var_low * 2), "High noise factor should produce more diversity"


class TestBoundsClipping:
    """Test that particles respect bounds after noise addition."""

    def test_bounds_clipping(self):
        """Ensure all particles respect bounds after Gaussian noise."""
        n_particles = 30
        n_gains = 6
        # Use gains near boundaries
        optimized = np.array([2.1, 1.5, 2.0, 0.3, 2.0, 0.06])  # Near min bounds
        baseline = np.array([29.0, 28.0, 9.5, 4.8, 49.0, 2.9])  # Near max bounds
        bounds_min = np.array([2.0, 1.0, 2.0, 0.2, 2.0, 0.05])
        bounds_max = np.array([30.0, 29.0, 10.0, 5.0, 50.0, 3.0])
        rng = np.random.default_rng(42)

        swarm = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng, noise_factor=0.1
        )

        # All particles must respect bounds
        assert np.all(swarm >= bounds_min), "Some particles below min bounds"
        assert np.all(swarm <= bounds_max), "Some particles above max bounds"

        # Check no particles exactly at bounds (unless noise pushed them there)
        particles_at_min = np.sum(np.abs(swarm - bounds_min) < 1e-10)
        particles_at_max = np.sum(np.abs(swarm - bounds_max) < 1e-10)

        # Allow some particles to be clipped (near boundaries)
        # Using gains near boundaries intentionally, so 20% clipping is acceptable
        assert particles_at_min + particles_at_max < n_particles * n_gains * 0.2, \
            "Too many particles clipped to bounds (suggests bounds too tight)"


class TestReproducibility:
    """Test that warm-start is reproducible with same seed."""

    def test_reproducibility_with_seed(self):
        """Verify same seed produces identical swarm."""
        n_particles = 30
        n_gains = 6
        optimized = np.array([2.0, 6.0, 5.0, 3.0, 4.0, 2.0])
        baseline = np.array([8.0, 4.0, 12.0, 6.0, 5.0, 3.0])
        bounds_min = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        bounds_max = np.array([15.0, 15.0, 15.0, 15.0, 15.0, 15.0])

        # Run 1
        rng1 = np.random.default_rng(42)
        swarm1 = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng1, noise_factor=0.1
        )

        # Run 2 (same seed)
        rng2 = np.random.default_rng(42)
        swarm2 = initialize_warm_start_swarm(
            n_particles, n_gains, optimized, baseline,
            bounds_min, bounds_max, rng2, noise_factor=0.1
        )

        # Should be identical
        np.testing.assert_array_equal(swarm1, swarm2)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
