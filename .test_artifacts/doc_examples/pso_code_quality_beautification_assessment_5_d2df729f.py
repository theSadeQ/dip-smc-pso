# Example from: docs\reports\pso_code_quality_beautification_assessment.md
# Index: 5
# Runnable: True
# Hash: d2df729f

# ✅ Excellent vectorized cost computation
ise = np.sum((x_b[:, :-1, :] ** 2 * dt_b[:, :, None]) * time_mask[:, :, None], axis=(1, 2))
u_sq = np.sum((u_b ** 2 * dt_b) * time_mask, axis=1)
du_sq = np.sum((du ** 2 * dt_b) * time_mask, axis=1)
sigma_sq = np.sum((sigma_b ** 2 * dt_b) * time_mask, axis=1)