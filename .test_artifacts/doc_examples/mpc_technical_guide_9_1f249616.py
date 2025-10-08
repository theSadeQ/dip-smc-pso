# Example from: docs\controllers\mpc_technical_guide.md
# Index: 9
# Runnable: True
# Hash: 1f249616

if max_du is not None:
    du = clip(u_cmd - u_last, -max_du, max_du)
    u_cmd = u_last + du