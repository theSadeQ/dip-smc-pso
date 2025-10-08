# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 16
# Runnable: False
# Hash: 66289caf

class UnifiedControllerFactory:
    """Unified factory bridging controller creation and PSO optimization.

    Provides single interface for creating controllers with optional PSO tuning,
    supporting both manual configuration and automated optimization workflows.

    Parameters
    ----------
    controller_type : str
        Controller type ('classical_smc', 'adaptive_smc', etc.).
    use_pso : bool, default=False
        Whether to use PSO optimization for parameter tuning.

    Examples
    --------
    >>> factory = UnifiedControllerFactory(
    ...     controller_type='classical_smc',
    ...     use_pso=True
    ... )
    >>> controller = factory.create(initial_gains=[...])
    """