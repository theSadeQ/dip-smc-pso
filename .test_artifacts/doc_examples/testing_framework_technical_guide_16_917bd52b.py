# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 16
# Runnable: True
# Hash: 917bd52b

class TestSMCFactory:
    """Test SMC controller factory."""

    def test_create_classical_smc(self):
        """Test factory creation of classical SMC."""
        from src.controllers.factory import SMCFactory, SMCType

        controller = SMCFactory.create_controller(
            SMCType.CLASSICAL,
            gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            max_force=100.0,
            boundary_layer=0.01
        )

        from src.controllers.smc.classic_smc import ClassicalSMC
        assert isinstance(controller, ClassicalSMC)
        assert controller.max_force == 100.0

    def test_create_all_controller_types(self):
        """Test factory can create all SMC types."""
        from src.controllers.factory import SMCFactory, SMCType

        gain_configs = {
            SMCType.CLASSICAL: [10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            SMCType.ADAPTIVE: [10.0, 8.0, 15.0, 12.0, 0.5],
            SMCType.SUPER_TWISTING: [25.0, 10.0, 15.0, 12.0, 20.0, 15.0],
            SMCType.HYBRID: [15.0, 12.0, 18.0, 15.0]
        }

        for smc_type, gains in gain_configs.items():
            controller = SMCFactory.create_controller(
                smc_type,
                gains=gains,
                max_force=100.0,
                boundary_layer=0.01
            )

            assert controller is not None
            assert hasattr(controller, 'compute_control')

    def test_invalid_controller_type(self):
        """Test factory raises error for invalid controller type."""
        from src.controllers.factory import SMCFactory

        with pytest.raises((ValueError, KeyError)):
            SMCFactory.create_controller(
                "invalid_type",
                gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0
            )