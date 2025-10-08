# Example from: docs\controllers\mpc_technical_guide.md
# Index: 34
# Runnable: True
# Hash: 8853fbfe

def check_linearization(x, x_eq=np.array([0, np.pi, np.pi, 0, 0, 0])):
    err = x - x_eq
    angle_err = np.max(np.abs(err[1:3]))
    if angle_err > 0.4:
        logger.warning(f"Large angle error: {angle_err:.3f} rad")
    return angle_err < 0.5