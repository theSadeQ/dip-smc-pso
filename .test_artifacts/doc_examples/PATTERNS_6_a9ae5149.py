# Example from: docs\PATTERNS.md
# Index: 6
# Runnable: False
# Hash: a9ae5149

# src/interfaces/monitoring/health_monitor.py (lines 85-100)

@dataclass
class ComponentHealth:
    """Health status of a system component."""
    component_name: str
    status: HealthStatus = HealthStatus.UNKNOWN
    check_results: List[HealthCheckResult] = field(default_factory=list)

    def update_status(self, new_status: HealthStatus) -> None:
        """Update component health status and notify observers."""
        if self.status != new_status:
            self.status = new_status
            self.last_check = time.time()
            self._notify_observers(new_status)

    def _notify_observers(self, status: HealthStatus) -> None:
        """Notify all registered observers of status change."""
        for observer in self._observers:
            observer.on_health_change(self.component_name, status)