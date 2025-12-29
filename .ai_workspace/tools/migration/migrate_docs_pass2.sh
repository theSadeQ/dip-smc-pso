#!/bin/bash
# Second pass - move remaining docs/ root files

# Theory/Math
mv docs/mathematical_algorithm_validation.md docs/theory/
mv docs/pso_gain_bounds_mathematical_foundations.md docs/theory/
mv docs/numerical_stability_guide.md docs/theory/
mv docs/theory_overview.md docs/theory/
mv docs/control_law_testing_standards.md docs/theory/
mv docs/safety_system_validation_protocols.md docs/theory/
mv docs/coverage_analysis_methodology.md docs/theory/
mv docs/benchmarks_methodology.md docs/theory/
mv docs/analysis_plan.md docs/theory/

# Optimization
mv docs/pso_configuration_schema_documentation.md docs/optimization/
mv docs/pso_factory_integration_patterns.md docs/optimization/
mv docs/PSO_INTEGRATION_GUIDE.md docs/optimization/
mv docs/pso_integration_system_architecture.md docs/optimization/
mv docs/pso_optimization_workflow_specifications.md docs/optimization/
mv docs/pso_optimization_workflow_user_guide.md docs/optimization/
mv docs/factory_integration_troubleshooting_guide.md docs/optimization/
mv docs/controller_pso_interface_api_documentation.md docs/optimization/

# Production
mv docs/production_documentation_summary.md docs/production/
mv docs/production_readiness_final.md docs/production/
mv docs/streamlit_dashboard_guide.md docs/production/

# Testing
mv docs/test_infrastructure_documentation.md docs/testing/
mv docs/test_infrastructure_validation_report.md docs/testing/
mv docs/test_protocols.md docs/testing/
mv docs/TESTING.md docs/testing/

# Architecture
mv docs/configuration_integration_documentation.md docs/architecture/
mv docs/memory_management_patterns.md docs/architecture/

# Guides
mv docs/fault_detection_guide.md docs/guides/
mv docs/fdi_threshold_calibration_methodology.md docs/guides/
mv docs/use_cases.md docs/guides/
mv docs/versioning_guide.md docs/guides/
mv docs/results_readme.md docs/guides/

# Reference
mv docs/PLANT_CONFIGURATION.md docs/reference/
mv docs/PACKAGE_CONTENTS.md docs/reference/
mv docs/symbols.md docs/reference/

# Meta
mv docs/ACADEMIC_INTEGRITY_STATEMENT.md docs/meta/
mv docs/bibliography.md docs/meta/
mv docs/CITATIONS_ACADEMIC.md docs/meta/
mv docs/documentation_structure.md docs/meta/
mv docs/NAVIGATION_STATUS_REPORT.md docs/meta/
mv docs/sitemap_cards.md docs/meta/
mv docs/sitemap_interactive.md docs/meta/
mv docs/sitemap_visual.md docs/meta/

echo "[OK] Pass 2 complete - moved 42 additional markdown files"
