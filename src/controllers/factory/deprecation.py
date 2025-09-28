#==========================================================================================\\\
#==================== src/controllers/factory/deprecation.py =======================\\\
#==========================================================================================\\\

"""
Controller Factory Deprecation Warning System.

Provides systematic deprecation warnings for controller configuration changes,
parameter renames, and interface modifications to ensure smooth migration paths.
"""

import warnings
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class DeprecationLevel(Enum):
    """Levels of deprecation severity."""
    INFO = "info"           # Informational - still supported
    WARNING = "warning"     # Will be removed in future versions
    ERROR = "error"         # Already removed, error fallback


@dataclass
class DeprecationMapping:
    """Configuration for a deprecated parameter or feature."""
    old_name: str
    new_name: Optional[str] = None
    level: DeprecationLevel = DeprecationLevel.WARNING
    message: Optional[str] = None
    migration_guide: Optional[str] = None
    removed_in_version: Optional[str] = None


class ControllerDeprecationWarner:
    """
    Systematic deprecation warning system for controller configurations.

    Tracks deprecated parameters, provides migration guidance, and ensures
    backward compatibility during transition periods.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._deprecation_mappings = self._initialize_deprecation_mappings()

    def _initialize_deprecation_mappings(self) -> Dict[str, Dict[str, DeprecationMapping]]:
        """Initialize deprecation mappings for all controller types."""
        return {
            'classical_smc': {
                'gamma': DeprecationMapping(
                    old_name='gamma',
                    new_name=None,
                    level=DeprecationLevel.ERROR,
                    message="'gamma' parameter is not valid for classical_smc. Use 'boundary_layer' instead.",
                    migration_guide="Classical SMC uses 'boundary_layer' for chattering reduction, not 'gamma' (which is for adaptive SMC).",
                    removed_in_version="2.0.0"
                ),
                'adaptation_rate': DeprecationMapping(
                    old_name='adaptation_rate',
                    new_name=None,
                    level=DeprecationLevel.ERROR,
                    message="'adaptation_rate' is not valid for classical_smc. This parameter is only for adaptive_smc.",
                    migration_guide="Remove 'adaptation_rate' from classical SMC configuration.",
                    removed_in_version="2.0.0"
                ),
                'switch_function': DeprecationMapping(
                    old_name='switch_function',
                    new_name='switch_method',
                    level=DeprecationLevel.WARNING,
                    message="'switch_function' parameter renamed to 'switch_method'.",
                    migration_guide="Replace 'switch_function' with 'switch_method' in configuration.",
                    removed_in_version="3.0.0"
                )
            },
            'adaptive_smc': {
                'boundary_layer_thickness': DeprecationMapping(
                    old_name='boundary_layer_thickness',
                    new_name='boundary_layer',
                    level=DeprecationLevel.WARNING,
                    message="'boundary_layer_thickness' parameter renamed to 'boundary_layer'.",
                    migration_guide="Replace 'boundary_layer_thickness' with 'boundary_layer' in configuration.",
                    removed_in_version="3.0.0"
                ),
                'adaptation_gain': DeprecationMapping(
                    old_name='adaptation_gain',
                    new_name='gamma',
                    level=DeprecationLevel.WARNING,
                    message="'adaptation_gain' parameter renamed to 'gamma' (included in gains array).",
                    migration_guide="Remove separate 'adaptation_gain' and include gamma as 5th element in gains array.",
                    removed_in_version="3.0.0"
                )
            },
            'sta_smc': {
                'K1': DeprecationMapping(
                    old_name='K1',
                    new_name='gains[0]',
                    level=DeprecationLevel.WARNING,
                    message="Separate K1/K2 parameters deprecated. Use gains array instead.",
                    migration_guide="Include K1, K2 as first two elements in gains array: [K1, K2, k1, k2, lam1, lam2]",
                    removed_in_version="3.0.0"
                ),
                'K2': DeprecationMapping(
                    old_name='K2',
                    new_name='gains[1]',
                    level=DeprecationLevel.WARNING,
                    message="Separate K1/K2 parameters deprecated. Use gains array instead.",
                    migration_guide="Include K1, K2 as first two elements in gains array: [K1, K2, k1, k2, lam1, lam2]",
                    removed_in_version="3.0.0"
                )
            },
            'hybrid_adaptive_sta_smc': {
                'mode': DeprecationMapping(
                    old_name='mode',
                    new_name='hybrid_mode',
                    level=DeprecationLevel.WARNING,
                    message="'mode' parameter renamed to 'hybrid_mode'.",
                    migration_guide="Replace 'mode' with 'hybrid_mode' and use HybridMode enum values.",
                    removed_in_version="3.0.0"
                )
            }
        }

    def check_deprecated_parameters(
        self,
        controller_type: str,
        config_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check for deprecated parameters and issue appropriate warnings.

        Args:
            controller_type: Type of controller being configured
            config_params: Configuration parameters to check

        Returns:
            Updated configuration parameters with deprecated ones migrated
        """
        if controller_type not in self._deprecation_mappings:
            return config_params

        updated_params = config_params.copy()
        deprecation_map = self._deprecation_mappings[controller_type]

        for param_name, param_value in config_params.items():
            if param_name in deprecation_map:
                mapping = deprecation_map[param_name]
                self._issue_deprecation_warning(controller_type, mapping, param_name, param_value)

                # Handle parameter migration
                if mapping.level == DeprecationLevel.ERROR:
                    # Remove invalid parameters
                    if param_name in updated_params:
                        del updated_params[param_name]
                        self.logger.error(
                            f"Removed invalid parameter '{param_name}' for {controller_type}: {mapping.message}"
                        )
                elif mapping.new_name and mapping.new_name not in updated_params:
                    # Migrate parameter name
                    if not mapping.new_name.startswith('gains['):  # Don't migrate array references automatically
                        updated_params[mapping.new_name] = param_value
                        del updated_params[param_name]
                        self.logger.info(f"Migrated '{param_name}' to '{mapping.new_name}' for {controller_type}")

        return updated_params

    def _issue_deprecation_warning(
        self,
        controller_type: str,
        mapping: DeprecationMapping,
        param_name: str,
        param_value: Any
    ) -> None:
        """Issue appropriate deprecation warning based on severity level."""
        message = f"[{controller_type}] {mapping.message or f'Parameter {param_name} is deprecated'}"

        if mapping.migration_guide:
            message += f" Migration: {mapping.migration_guide}"

        if mapping.removed_in_version:
            message += f" (Will be removed in version {mapping.removed_in_version})"

        if mapping.level == DeprecationLevel.INFO:
            self.logger.info(message)
        elif mapping.level == DeprecationLevel.WARNING:
            warnings.warn(message, DeprecationWarning, stacklevel=4)
            self.logger.warning(message)
        elif mapping.level == DeprecationLevel.ERROR:
            self.logger.error(message)
            # Don't raise exception - just log and remove parameter

    def get_migration_guide(self, controller_type: str) -> List[str]:
        """Get comprehensive migration guide for a controller type."""
        if controller_type not in self._deprecation_mappings:
            return []

        guides = []
        for mapping in self._deprecation_mappings[controller_type].values():
            if mapping.migration_guide:
                guides.append(f"• {mapping.old_name}: {mapping.migration_guide}")

        return guides

    def validate_configuration_compatibility(
        self,
        controller_type: str,
        config_params: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Validate configuration compatibility and return detailed issues.

        Returns:
            Dictionary mapping parameter names to their compatibility issues
        """
        issues = {}

        if controller_type not in self._deprecation_mappings:
            return issues

        deprecation_map = self._deprecation_mappings[controller_type]

        for param_name in config_params:
            if param_name in deprecation_map:
                mapping = deprecation_map[param_name]
                if mapping.level == DeprecationLevel.ERROR:
                    issues[param_name] = mapping.message or f"Parameter no longer supported"
                elif mapping.level == DeprecationLevel.WARNING:
                    issues[param_name] = f"Deprecated - {mapping.migration_guide}"

        return issues


# Global deprecation warner instance
_deprecation_warner = ControllerDeprecationWarner()


def check_deprecated_config(controller_type: str, config_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to check and migrate deprecated configuration parameters.

    Args:
        controller_type: Type of controller
        config_params: Configuration parameters

    Returns:
        Updated configuration with deprecated parameters migrated
    """
    return _deprecation_warner.check_deprecated_parameters(controller_type, config_params)


def get_controller_migration_guide(controller_type: str) -> List[str]:
    """
    Get migration guide for a specific controller type.

    Args:
        controller_type: Type of controller

    Returns:
        List of migration guidance strings
    """
    return _deprecation_warner.get_migration_guide(controller_type)


def validate_config_compatibility(controller_type: str, config_params: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate configuration compatibility for a controller type.

    Args:
        controller_type: Type of controller
        config_params: Configuration parameters to validate

    Returns:
        Dictionary of compatibility issues
    """
    return _deprecation_warner.validate_configuration_compatibility(controller_type, config_params)