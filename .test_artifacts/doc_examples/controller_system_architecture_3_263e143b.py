# Example from: docs\architecture\controller_system_architecture.md
# Index: 3
# Runnable: False
# Hash: 263e143b

class ConfigurationBridge:
    """Bridge between YAML configuration and controller parameters."""

    @staticmethod
    def map_config_to_controller(
        controller_type: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map generic configuration to controller-specific parameters."""

        mapping_strategies = {
            'classical_smc': ClassicalSMCConfigMapper,
            'adaptive_smc': AdaptiveSMCConfigMapper,
            'sta_smc': STASMCConfigMapper,
            'hybrid_adaptive_sta_smc': HybridSMCConfigMapper
        }

        mapper = mapping_strategies.get(controller_type)
        if not mapper:
            raise ValueError(f"No configuration mapper for {controller_type}")

        return mapper.map_config(config)