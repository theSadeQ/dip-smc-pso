# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 25
# Runnable: False
# Hash: 2812c32e

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def parallel_controller_creation_safe(controller_configs):
    """Safe parallel controller creation with reduced contention."""

    # Strategy 1: Batch creation to reduce lock contention
    batch_size = 4  # Limit concurrent factory calls
    results = []

    def create_controller_batch(config_batch):
        """Create a batch of controllers."""
        batch_results = []

        for config in config_batch:
            try:
                controller = create_controller(**config)
                batch_results.append(('success', controller))
            except Exception as e:
                batch_results.append(('error', str(e)))

        return batch_results

    # Split configs into batches
    batches = [
        controller_configs[i:i+batch_size]
        for i in range(0, len(controller_configs), batch_size)
    ]

    # Process batches sequentially to avoid lock contention
    for batch in batches:
        batch_results = create_controller_batch(batch)
        results.extend(batch_results)

    return results

# Usage
configs = [
    {'controller_type': 'classical_smc', 'gains': [20, 15, 12, 8, 35, 5]},
    {'controller_type': 'adaptive_smc', 'gains': [25, 18, 15, 10, 4]},
    # ... more configs
]

results = parallel_controller_creation_safe(configs)