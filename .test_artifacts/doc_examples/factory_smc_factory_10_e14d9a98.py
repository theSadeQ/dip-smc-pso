# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 10
# Runnable: True
# Hash: e14d9a98

config = (SMCConfigBuilder()
    .with_gains([10, 8, 15, 12, 50, 5])
    .with_max_force(100.0)
    .build())