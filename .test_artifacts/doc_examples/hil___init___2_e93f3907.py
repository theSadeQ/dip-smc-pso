# Example from: docs\reference\interfaces\hil___init__.md
# Index: 2
# Runnable: True
# Hash: e93f3907

from src.interfaces import hil
from threading import Thread

# Server on one thread
def run_server():
    server = hil.PlantServer(
        cfg=config,
        bind_addr=("0.0.0.0", 5555),
        dt=0.01
    )
    server.start()

# Client on another thread
def run_client():
    time.sleep(1.0)  # Wait for server to start
    client = hil.HILControllerClient(
        cfg=config,
        plant_addr=("127.0.0.1", 5555),
        bind_addr=("127.0.0.1", 0),
        dt=0.01,
        steps=5000
    )
    client.run()

# Run distributed
t1 = Thread(target=run_server)
t2 = Thread(target=run_client)
t1.start()
t2.start()
t1.join()
t2.join()