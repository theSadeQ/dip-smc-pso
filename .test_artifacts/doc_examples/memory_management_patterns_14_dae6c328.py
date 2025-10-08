# Example from: docs\memory_management_patterns.md
# Index: 14
# Runnable: True
# Hash: dae6c328

import tracemalloc
import gc

tracemalloc.start()

# Create many controllers
controllers = []
for i in range(1000):
    c = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100, boundary_layer=0.01)
    controllers.append(c)

snapshot1 = tracemalloc.take_snapshot()

# Clear controllers
controllers.clear()
gc.collect()

snapshot2 = tracemalloc.take_snapshot()
diff = snapshot2.compare_to(snapshot1, 'lineno')

# Should show memory decrease
for stat in diff[:10]:
    print(stat)