# Example from: docs\controllers\mpc_technical_guide.md
# Index: 33
# Runnable: True
# Hash: fc9c03d7

status = prob.status
if status != cp.OPTIMAL:
    logger.warning(f"MPC status: {status}")
    logger.debug(f"Objective value: {prob.value}")
    logger.debug(f"Constraint violations: {[c.violation() for c in prob.constraints]}")