# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 4
# Runnable: True
# Hash: 272a77c2

class Controller(ABC):
    @abstractmethod
    def compute_control(self, state, state_vars, history):
        """Subclasses MUST implement this."""
        pass

    def reset(self):
        """Default implementation (optional override)."""
        return self.initialize_history()