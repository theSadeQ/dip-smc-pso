# Example from: docs\reference\optimization\integration_pso_factory_bridge.md
# Index: 1
# Runnable: False
# Hash: 98ede236

# example-metadata:
# runnable: false

def particle_to_controller(particle: np.ndarray) -> Controller:
    gains = {
        'k1': particle[0],
        'k2': particle[1],
        # ...
    }
    return ControllerFactory.create(gains)