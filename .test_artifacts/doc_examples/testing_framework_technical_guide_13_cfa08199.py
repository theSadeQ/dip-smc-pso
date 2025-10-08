# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 13
# Runnable: False
# Hash: cfa08199

# example-metadata:
# runnable: false

class TestClassicalSMCInitialization:
    """Test Classical SMC controller initialization."""

    def test_valid_initialization(self):
        """Test successful initialization with valid parameters."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = ClassicalSMC(
            gains=gains,
            max_force=100.0,
            boundary_layer=0.01,
            dt=0.01
        )

        # Verify all parameters stored correctly
        assert controller.k1 == 10.0
        assert controller.k2 == 8.0
        assert controller.lam1 == 15.0
        assert controller.lam2 == 12.0
        assert controller.K == 50.0
        assert controller.kd == 5.0
        assert controller.max_force == 100.0
        assert controller.boundary_layer == 0.01
        assert controller.dt == 0.01

    def test_invalid_gains_negative(self):
        """Test that negative gains are rejected."""
        with pytest.raises(ValueError, match="must be positive"):
            ClassicalSMC(
                gains=[10.0, -8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0,
                boundary_layer=0.01
            )

    def test_invalid_gains_zero(self):
        """Test that zero gains are rejected."""
        with pytest.raises(ValueError, match="must be positive"):
            ClassicalSMC(
                gains=[0.0, 8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0,
                boundary_layer=0.01
            )

    def test_invalid_max_force(self):
        """Test that invalid max_force is rejected."""
        with pytest.raises(ValueError, match="max_force must be positive"):
            ClassicalSMC(
                gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=-100.0,
                boundary_layer=0.01
            )

    def test_invalid_boundary_layer(self):
        """Test that invalid boundary_layer is rejected."""
        with pytest.raises(ValueError, match="boundary_layer must be positive"):
            ClassicalSMC(
                gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0,
                boundary_layer=0.0
            )