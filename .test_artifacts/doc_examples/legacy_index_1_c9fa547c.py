# Example from: docs\implementation\legacy_index.md
# Index: 1
# Runnable: False
# Hash: c9fa547c

# example-metadata:
# runnable: false

def sliding_surface(self, x: np.ndarray) -> float:
    """
    Compute sliding surface value s(x) = Sx.

    Based on equation {eq}`eq:sliding_surface_design` from SMC theory.

    Parameters
    ----------
    x : np.ndarray, shape (6,)
        State vector [q, q_dot]

    Returns
    -------
    s : float
        Sliding surface value

    See Also
    --------
    theory.smc_theory_complete : Theoretical foundation
    """
    return self.S @ x  # Implements eq:sliding_surface_design