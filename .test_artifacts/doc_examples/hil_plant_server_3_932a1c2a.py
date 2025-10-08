# Example from: docs\reference\interfaces\hil_plant_server.md
# Index: 3
# Runnable: True
# Hash: 932a1c2a

from threading import Thread
from src.interfaces.hil import PlantServer

def run_server(port, max_steps):
    server = PlantServer(
        cfg=config,
        bind_addr=("127.0.0.1", port),
        dt=0.01,
        max_steps=max_steps
    )
    server.start()
    server.close()

# Run multiple servers for parallel testing
threads = []
for port in [5555, 5556, 5557]:
    t = Thread(target=run_server, args=(port, 5000))
    t.start()
    threads.append(t)

# Wait for all servers to complete
for t in threads:
    t.join()

print("All parallel tests complete")