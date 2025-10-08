# Example from: docs\reference\simulation\orchestrators_batch.md
# Index: 8
# Runnable: True
# Hash: 76e79aac

import time
start = time.time()
result = instance.process(data)
elapsed = time.time() - start
print(f"Execution time: {elapsed:.4f} s")