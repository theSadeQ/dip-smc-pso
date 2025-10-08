# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 13
# Runnable: False
# Hash: 6ff6b911

class ResilientDataExchange:
    """Resilient data exchange interface with fault tolerance.

    Provides multi-source data exchange with automatic failover, retry logic,
    and graceful degradation for hardware-in-the-loop systems.

    Parameters
    ----------
    primary_source : str
        Primary data source identifier.
    fallback_sources : List[str], optional
        Ordered list of fallback sources.
    retry_attempts : int, default=3
        Number of retry attempts before failover.
    timeout : float, default=1.0
        Timeout for each data exchange attempt (seconds).

    Examples
    --------
    >>> exchange = ResilientDataExchange(
    ...     primary_source='udp://192.168.1.100:5000',
    ...     fallback_sources=['serial:COM3', 'tcp://localhost:8000']
    ... )
    """