# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 5
# Runnable: False
# Hash: cf403d09

# example-metadata:
# runnable: false

# Example high-quality test with comprehensive coverage
def test_pso_tuner_initialization(self, minimal_config, mock_controller_factory):
    """Test PSOTuner initialization with comprehensive validation."""
    tuner = PSOTuner(
        controller_factory=mock_controller_factory,
        config=minimal_config,
        seed=42
    )

    assert tuner.seed == 42
    assert tuner.instability_penalty > 0
    assert tuner.combine_weights == (0.7, 0.3)
    assert tuner.normalisation_threshold > 0