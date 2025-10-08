# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 14
# Runnable: False
# Hash: 54a36f1b

# example-metadata:
# runnable: false

class NetworkMessage:
    """Network message container for control system communication.

    Encapsulates state, control, and metadata for real-time HIL communication.

    Attributes
    ----------
    timestamp : float
        Message creation timestamp (seconds since epoch).
    state : np.ndarray
        System state vector.
    control : float
        Control input value.
    metadata : Dict[str, Any]
        Additional message metadata.
    """