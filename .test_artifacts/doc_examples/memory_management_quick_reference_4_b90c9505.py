# Example from: docs\memory_management_quick_reference.md
# Index: 4
# Runnable: True
# Hash: b90c9505

import psutil
import os

process = psutil.Process(os.getpid())
memory_mb = process.memory_info().rss / 1024 / 1024
print(f"Memory usage: {memory_mb:.1f}MB")