# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 29
# Runnable: True
# Hash: 1f57a84a

def create_comparison_study_controllers():
    # Manual creation for each controller type
    controllers = {
        'classical': create_controller('classical_smc', gains=[10,8,15,12,50,5]),
        'adaptive': create_controller('adaptive_smc', gains=[10,8,15,12,0.5]),
        'sta': create_controller('sta_smc', gains=[25,10,15,12,20,15]),
        'hybrid': create_controller('hybrid_adaptive_sta_smc', gains=[15,12,18,15])
    }
    return controllers