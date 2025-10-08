# Example from: docs\reference\interfaces\hil_real_time_sync.md
# Index: 2
# Runnable: True
# Hash: 07b887fe

from src.interfaces.hil.real_time_sync import ClockSync

# Create clock synchronizer
clock_sync = ClockSync()

# Client-server clock sync
def client_sync():
    t1 = time.time()
    # Send to server
    t2, t3 = server.get_timestamps()
    t4 = time.time()

    # Compute offset
    offset = clock_sync.compute_offset(t1, t2, t3, t4)
    print(f"Clock offset: {offset * 1000:.2f} ms")

client_sync()