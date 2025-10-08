# Example from: docs\guides\tutorials\tutorial-05-research-workflow.md
# Index: 4
# Runnable: False
# Hash: 5ff8ff3a

#!/usr/bin/env python
"""Generate automated research report."""

import pandas as pd
import yaml

# Load results and metadata
df = pd.read_csv('experiments/robustness_study/results/monte_carlo_results.csv')
with open('experiments/robustness_study/metadata.yaml') as f:
    metadata = yaml.safe_load(f)

# Generate markdown report
report = f"""
# {metadata['study']['title']}

**Authors:** {', '.join(metadata['study']['authors'])}
**Date:** {metadata['study']['date']}
**Version:** {metadata['study']['version']}

---

## Abstract

This study compares the robustness of Classical SMC and Hybrid Adaptive STA-SMC
controllers under mass parameter uncertainty for a double-inverted pendulum system.
Monte Carlo simulations (N={metadata['methods']['monte_carlo']['n_trials']}) were
conducted across 5 parameter variation scenarios. Results indicate Hybrid Adaptive
STA-SMC achieves {improvement:.1f}% better robustness (p < 0.001, Cohen's d = {cohens_d:.2f}).

## Methodology

### Controllers Tested
{chr(10).join(f"- **{c['name']}**: {c['implementation']}" for c in metadata['methods']['controllers'])}

### Experimental Scenarios
{chr(10).join(f"- {var}" for var in metadata['methods']['scenarios']['parameter_variations'])}

### Statistical Analysis
- Hypothesis Test: {metadata['statistical_analysis']['hypothesis_test']}
- Significance Level: α = {metadata['statistical_analysis']['significance_level']}
- Effect Size Metric: {metadata['statistical_analysis']['effect_size']}

## Results

### Summary Statistics
{{summary_table}}

### Hypothesis Test Results
{{hypothesis_results}}

## Conclusions

{{conclusions}}

## Reproducibility
All code, data, and configurations are available in `experiments/robustness_study/`.
Random seeds logged for each trial. Framework version: {metadata['reproducibility']['framework_version']}.

---
"""

# Fill in results (placeholder for actual computation)
# ... (run analysis and populate results)

# Save report
with open('experiments/robustness_study/REPORT.md', 'w') as f:
    f.write(report)

print("Report generated: experiments/robustness_study/REPORT.md")