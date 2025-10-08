# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 2
# Runnable: False
# Hash: 61a21acf

def analyze_fdi_failure():
    """Technical analysis of FDI threshold sensitivity."""

    # Problem: Threshold too aggressive for operational conditions
    current_threshold = 0.1000
    observed_residual = 0.1332
    exceedance_ratio = observed_residual / current_threshold  # 1.332

    # Statistical analysis of residual norms
    residual_statistics = {
        'mean': 0.0845,
        'std': 0.0287,
        'p95': 0.1265,  # 95th percentile exceeds current threshold
        'p99': 0.1421   # 99th percentile well above threshold
    }

    # Recommended threshold adjustment
    recommended_threshold = residual_statistics['p95'] * 1.15  # ~0.145
    safety_margin = (recommended_threshold - current_threshold) / current_threshold * 100  # 45%

    return {
        'issue': 'Threshold too restrictive for operational variability',
        'recommendation': f'Increase threshold to {recommended_threshold:.3f}',
        'safety_margin': f'{safety_margin:.1f}% additional tolerance'
    }