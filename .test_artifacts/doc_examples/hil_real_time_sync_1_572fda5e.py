# Example from: docs\reference\interfaces\hil_real_time_sync.md
# Index: 1
# Runnable: True
# Hash: 572fda5e

from src.interfaces.hil.real_time_sync import RealTimeSync

# Initialize synchronizer
sync = RealTimeSync(
    processes=["plant", "controller"],
    target_dt=0.01,  # 10 ms control period
    tolerance=0.001  # 1 ms tolerance
)

# Synchronize processes
sync.synchronize()

# Plant and controller now running at same rate