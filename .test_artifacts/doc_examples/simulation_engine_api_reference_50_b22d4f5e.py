# Example from: docs\api\simulation_engine_api_reference.md
# Index: 50
# Runnable: True
# Hash: b22d4f5e

@classmethod
def create_integrator(
    cls,
    integrator_type: str,
    dt: float = 0.01,
    **kwargs: Any
) -> BaseIntegrator:
    """Create integrator instance of specified type."""