# Example from: docs\reports\GITHUB_ISSUE_6_RESOLUTION_REPORT.md
# Index: 1
# Runnable: True
# Hash: 8784e056

# Fixed registry consistency test to handle optional controllers
if controller_info.get('class') is not None:
    assert controller_type in available_types