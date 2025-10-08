# Example from: docs\fault_detection_system_documentation.md
# Index: 25
# Runnable: True
# Hash: cb6f45c0

def recommend_threshold(baseline_stats, target_far=0.01):
    """Recommend threshold based on desired false alarm rate."""

    # For normal distribution, use quantile-based approach
    from scipy import stats
    z_score = stats.norm.ppf(1 - target_far)  # Z-score for desired FAR

    recommended_threshold = baseline_stats['mean'] + z_score * baseline_stats['std']

    print(f"Recommended threshold: {recommended_threshold:.4f}")
    print(f"This targets {target_far:.1%} false alarm rate")

    return recommended_threshold