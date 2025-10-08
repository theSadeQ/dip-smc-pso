# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 30
# Runnable: True
# Hash: 4b2b395d

def create_comparison_study_controllers():
    # Batch creation with validation
    gains_dict = {
        'classical': [10, 8, 15, 12, 50, 5],
        'adaptive': [10, 8, 15, 12, 0.5],
        'sta': [25, 10, 15, 12, 20, 15],
        'hybrid': [15, 12, 18, 15]
    }
    return create_all_smc_controllers(gains_dict, max_force=100.0)