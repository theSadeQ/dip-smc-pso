# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 1
# Runnable: False
# Hash: 57bd28af

# example-metadata:
# runnable: false

# Data Loading (2 functions)
load_json_safe()                     # Safe JSON loading with error handling
convert_to_json_serializable()       # NumPy/Pandas to JSON type converter

# Data Parsing (4 functions)
parse_controller_performance()       # Main controller metrics parser
parse_pso_sensitivity()              # PSO parameter sensitivity parser
parse_numerical_stability()          # Matrix regularization metrics parser
parse_control_accuracy()             # Control accuracy parser (handles failures)

# Statistical Analysis (3 functions)
compute_settling_time_stats()        # Settling time with 95% CI
perform_anova_test()                 # One-way ANOVA for controller comparison
compute_pairwise_ttests()            # Welch's t-tests for pairwise comparison

# Chart.js Generation (5 functions)
generate_settling_time_chart()       # Bar chart with error bars
generate_computational_efficiency_chart()  # Grouped bar chart
generate_stability_scores_chart()    # Radar chart
generate_pso_sensitivity_heatmap()   # Sensitivity bar chart
generate_overshoot_analysis_chart()  # Box plot

# Main Execution (1 function)
main()                               # Orchestration workflow