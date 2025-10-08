# Example from: docs\reference\interfaces\hil_real_time_sync.md
# Index: 3
# Runnable: True
# Hash: 33f9c6f7

from src.interfaces.hil.real_time_sync import BarrierSync
from threading import Thread

# Create barrier
barrier = BarrierSync(n_processes=2)

def plant_process():
    for step in range(1000):
        # Compute dynamics
        plant.step()
        # Wait for controller
        barrier.wait()

def controller_process():
    for step in range(1000):
        # Compute control
        controller.compute()
        # Wait for plant
        barrier.wait()

# Run synchronized
t1 = Thread(target=plant_process)
t2 = Thread(target=controller_process)
t1.start()
t2.start()
t1.join()
t2.join()