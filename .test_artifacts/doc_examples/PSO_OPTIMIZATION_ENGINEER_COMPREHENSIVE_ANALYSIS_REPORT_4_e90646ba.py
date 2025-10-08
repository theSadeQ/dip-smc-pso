# Example from: docs\reports\PSO_OPTIMIZATION_ENGINEER_COMPREHENSIVE_ANALYSIS_REPORT.md
# Index: 4
# Runnable: True
# Hash: e90646ba

def _combine_costs(self, costs):
    """Multi-objective cost combination"""
    mean_w, max_w = self.combine_weights  # (0.7, 0.3)
    return mean_w * costs.mean(axis=0) + max_w * costs.max(axis=0)