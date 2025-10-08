# Example from: docs\factory\deprecation_management.md
# Index: 7
# Runnable: True
# Hash: 650bf32d

class ControllerDeprecationWarner:
    """
    Enterprise-grade deprecation warning system with comprehensive tracking.

    Features:
    - Multi-level deprecation severity
    - Automatic parameter migration
    - Detailed migration guidance
    - Usage analytics and reporting
    - Integration with logging systems
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._deprecation_mappings = self._initialize_deprecation_mappings()
        self._usage_statistics = defaultdict(int)
        self._migration_history = []

    def _initialize_deprecation_mappings(self) -> Dict[str, Dict[str, DeprecationMapping]]:
        """Initialize comprehensive deprecation mappings for all controller types."""
        return {
            'classical_smc': CLASSICAL_SMC_DEPRECATIONS,
            'adaptive_smc': ADAPTIVE_SMC_DEPRECATIONS,
            'sta_smc': STA_SMC_DEPRECATIONS,
            'hybrid_adaptive_sta_smc': HYBRID_SMC_DEPRECATIONS
        }

    def check_deprecated_parameters(
        self,
        controller_type: str,
        config_params: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[DeprecationWarning]]:
        """
        Check for deprecated parameters and perform migration.

        Args:
            controller_type: Type of controller being configured
            config_params: Configuration parameters to check

        Returns:
            Tuple of (migrated_params, warning_list)
        """
        if controller_type not in self._deprecation_mappings:
            return config_params, []

        updated_params = config_params.copy()
        warnings_issued = []
        deprecation_map = self._deprecation_mappings[controller_type]

        for param_name, param_value in config_params.items():
            if param_name in deprecation_map:
                mapping = deprecation_map[param_name]

                # Track usage statistics
                self._usage_statistics[f"{controller_type}.{param_name}"] += 1

                # Issue appropriate warning
                warning = self._issue_deprecation_warning(
                    controller_type, mapping, param_name, param_value
                )
                warnings_issued.append(warning)

                # Perform migration if enabled
                if mapping.auto_migrate:
                    migration_result = self._perform_automatic_migration(
                        updated_params, mapping, param_name, param_value
                    )

                    if migration_result.success:
                        self._record_migration(controller_type, mapping, migration_result)
                    else:
                        self.logger.error(f"Migration failed for {param_name}: {migration_result.error}")

        return updated_params, warnings_issued

    def _issue_deprecation_warning(
        self,
        controller_type: str,
        mapping: DeprecationMapping,
        param_name: str,
        param_value: Any
    ) -> DeprecationWarning:
        """Issue comprehensive deprecation warning with detailed guidance."""

        # Construct detailed message
        message_parts = [
            f"[{controller_type}] {mapping.message or f'Parameter {param_name} is deprecated'}"
        ]

        if mapping.migration_guide:
            message_parts.append(f"Migration: {mapping.migration_guide}")

        if mapping.removed_in_version:
            message_parts.append(f"Will be removed in version {mapping.removed_in_version}")

        if mapping.new_name:
            message_parts.append(f"Use '{mapping.new_name}' instead")

        full_message = " | ".join(message_parts)

        # Create warning object with metadata
        warning = DeprecationWarning(full_message)
        warning.controller_type = controller_type
        warning.old_parameter = param_name
        warning.new_parameter = mapping.new_name
        warning.deprecation_level = mapping.level
        warning.migration_guide = mapping.migration_guide

        # Issue warning based on severity
        if mapping.level == DeprecationLevel.INFO:
            self.logger.info(full_message)
        elif mapping.level == DeprecationLevel.WARNING:
            warnings.warn(full_message, DeprecationWarning, stacklevel=5)
            self.logger.warning(full_message)
        elif mapping.level == DeprecationLevel.ERROR:
            self.logger.error(full_message)

        return warning

    def _perform_automatic_migration(
        self,
        params: Dict[str, Any],
        mapping: DeprecationMapping,
        old_name: str,
        old_value: Any
    ) -> 'MigrationResult':
        """Perform automatic parameter migration with validation."""

        try:
            # Validate value if validation function provided
            if mapping.validation_function and not mapping.validation_function(old_value):
                return MigrationResult(
                    success=False,
                    error=f"Value {old_value} failed validation for {old_name}"
                )

            # Handle different migration scenarios
            if mapping.level == DeprecationLevel.ERROR:
                # Remove invalid parameters
                if old_name in params:
                    del params[old_name]
                    return MigrationResult(
                        success=True,
                        action=f"Removed invalid parameter '{old_name}'"
                    )

            elif mapping.new_name and mapping.new_name not in params:
                # Handle parameter renaming
                if isinstance(mapping.new_name, str):
                    # Simple rename
                    if not mapping.new_name.startswith('gains['):
                        params[mapping.new_name] = old_value
                        del params[old_name]
                        return MigrationResult(
                            success=True,
                            action=f"Migrated '{old_name}' to '{mapping.new_name}'"
                        )
                    else:
                        # Complex migration to gains array
                        return self._migrate_to_gains_array(params, mapping, old_name, old_value)

                elif isinstance(mapping.new_name, list):
                    # Split parameter into multiple new parameters
                    return self._migrate_split_parameter(params, mapping, old_name, old_value)

            return MigrationResult(success=True, action="No migration needed")

        except Exception as e:
            return MigrationResult(success=False, error=str(e))

    def _migrate_to_gains_array(
        self,
        params: Dict[str, Any],
        mapping: DeprecationMapping,
        old_name: str,
        old_value: Any
    ) -> 'MigrationResult':
        """Migrate parameter to gains array position."""

        # Extract array index from new_name (e.g., 'gains[4]' -> 4)
        import re
        match = re.search(r'gains\[(\d+)\]', mapping.new_name)
        if not match:
            return MigrationResult(success=False, error="Invalid gains array specification")

        index = int(match.group(1))

        # Ensure gains array exists and is large enough
        if 'gains' not in params:
            params['gains'] = [1.0] * (index + 1)
        elif len(params['gains']) <= index:
            params['gains'].extend([1.0] * (index + 1 - len(params['gains'])))

        # Set the value
        params['gains'][index] = old_value
        del params[old_name]

        return MigrationResult(
            success=True,
            action=f"Migrated '{old_name}' to gains[{index}]"
        )

    def _migrate_split_parameter(
        self,
        params: Dict[str, Any],
        mapping: DeprecationMapping,
        old_name: str,
        old_value: Any
    ) -> 'MigrationResult':
        """Migrate parameter that splits into multiple new parameters."""

        if old_name == 'estimate_bounds' and isinstance(old_value, (list, tuple)) and len(old_value) == 2:
            params['K_min'] = old_value[0]
            params['K_max'] = old_value[1]
            del params[old_name]
            return MigrationResult(
                success=True,
                action=f"Split '{old_name}' into K_min and K_max"
            )

        return MigrationResult(
            success=False,
            error=f"Don't know how to split parameter {old_name}"
        )

    def _record_migration(
        self,
        controller_type: str,
        mapping: DeprecationMapping,
        result: 'MigrationResult'
    ) -> None:
        """Record migration for analytics and reporting."""
        migration_record = {
            'timestamp': time.time(),
            'controller_type': controller_type,
            'old_parameter': mapping.old_name,
            'new_parameter': mapping.new_name,
            'deprecation_level': mapping.level.value,
            'migration_action': result.action,
            'success': result.success
        }
        self._migration_history.append(migration_record)

    def get_migration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive migration and usage statistics."""
        return {
            'deprecated_parameter_usage': dict(self._usage_statistics),
            'migration_history': self._migration_history,
            'total_migrations': len(self._migration_history),
            'successful_migrations': sum(1 for m in self._migration_history if m['success']),
            'migration_by_controller': self._group_migrations_by_controller(),
            'most_used_deprecated_params': self._get_most_used_deprecated()
        }

    def _group_migrations_by_controller(self) -> Dict[str, int]:
        """Group migration statistics by controller type."""
        controller_stats = defaultdict(int)
        for migration in self._migration_history:
            controller_stats[migration['controller_type']] += 1
        return dict(controller_stats)

    def _get_most_used_deprecated(self) -> List[Tuple[str, int]]:
        """Get most frequently used deprecated parameters."""
        return sorted(self._usage_statistics.items(), key=lambda x: x[1], reverse=True)[:10]

    def generate_deprecation_report(self) -> Dict[str, Any]:
        """Generate comprehensive deprecation usage report."""
        return {
            'report_timestamp': time.time(),
            'statistics': self.get_migration_statistics(),
            'recommendations': self._generate_migration_recommendations(),
            'upcoming_removals': self._get_upcoming_removals(),
            'migration_health_score': self._calculate_migration_health_score()
        }

    def _generate_migration_recommendations(self) -> List[str]:
        """Generate recommendations based on usage patterns."""
        recommendations = []

        # Check for high usage of deprecated parameters
        for param, count in self._get_most_used_deprecated():
            if count > 10:
                recommendations.append(
                    f"High usage of deprecated parameter '{param}' ({count} times). "
                    "Consider updating configurations to use new parameter names."
                )

        # Check for failed migrations
        failed_migrations = [m for m in self._migration_history if not m['success']]
        if failed_migrations:
            recommendations.append(
                f"{len(failed_migrations)} migration failures detected. "
                "Review migration logs and update configurations manually."
            )

        return recommendations

    def _get_upcoming_removals(self) -> List[Dict[str, Any]]:
        """Get list of parameters scheduled for removal."""
        upcoming = []
        for controller_type, mappings in self._deprecation_mappings.items():
            for param_name, mapping in mappings.items():
                if mapping.level == DeprecationLevel.WARNING and mapping.removed_in_version:
                    upcoming.append({
                        'controller_type': controller_type,
                        'parameter': param_name,
                        'removal_version': mapping.removed_in_version,
                        'migration_guide': mapping.migration_guide
                    })
        return upcoming

    def _calculate_migration_health_score(self) -> float:
        """Calculate overall migration health score (0-100)."""
        if not self._migration_history:
            return 100.0

        successful_migrations = sum(1 for m in self._migration_history if m['success'])
        success_rate = successful_migrations / len(self._migration_history)

        # Factor in usage of deprecated parameters
        deprecated_usage = sum(self._usage_statistics.values())
        usage_penalty = min(deprecated_usage * 0.1, 30.0)  # Max 30 point penalty

        health_score = (success_rate * 100) - usage_penalty
        return max(0.0, min(100.0, health_score))

@dataclass
class MigrationResult:
    """Result of automatic parameter migration."""
    success: bool
    action: Optional[str] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)