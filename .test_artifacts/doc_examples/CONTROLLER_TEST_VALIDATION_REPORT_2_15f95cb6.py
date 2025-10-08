# Example from: docs\reports\CONTROLLER_TEST_VALIDATION_REPORT.md
# Index: 2
# Runnable: True
# Hash: 15f95cb6

# Fixed config instantiation across all test files
config = FullDIPConfig.create_default()  # Fixed: was FullDIPConfig()
config = LowRankDIPConfig.create_default()  # Fixed: was LowRankDIPConfig()