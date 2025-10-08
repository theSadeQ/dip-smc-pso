# Example from: docs\technical\integration_protocols.md
# Index: 11
# Runnable: False
# Hash: 3da72066

# example-metadata:
# runnable: false

class DataExchangeBus:
    """Central data exchange bus for cross-domain communication."""

    def __init__(self):
        self._subscribers = {}
        self._message_queue = []

    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to data topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    def publish(self, topic: str, data: Any):
        """Publish data to topic."""
        if topic in self._subscribers:
            for callback in self._subscribers[topic]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Subscriber callback failed: {e}")

    def get_data_schema(self, topic: str) -> Dict[str, Any]:
        """Get data schema for topic."""
        schemas = {
            'system_state': SystemState.__annotations__,
            'control_action': ControlAction.__annotations__,
            'simulation_result': SimulationResult.__annotations__,
            'optimization_result': OptimizationResult.__annotations__
        }
        return schemas.get(topic, {})

# Global data exchange bus instance
data_bus = DataExchangeBus()