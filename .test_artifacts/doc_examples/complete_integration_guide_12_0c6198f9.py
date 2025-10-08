# Example from: docs\workflows\complete_integration_guide.md
# Index: 12
# Runnable: True
# Hash: 0c6198f9

# Distributed control system
from src.distributed import ControllerNode, CoordinatorNode

def distributed_control_setup():
    """Set up distributed control architecture."""

    # Coordinator node
    coordinator = CoordinatorNode(
        port=8000,
        controllers=['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc'],
        load_balancing='performance_based'
    )

    # Controller nodes
    nodes = []
    for i, controller_type in enumerate(['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']):
        node = ControllerNode(
            node_id=f"node_{i}",
            controller_type=controller_type,
            coordinator_address="localhost:8000",
            port=8001 + i
        )
        nodes.append(node)

    # Start distributed system
    coordinator.start()
    for node in nodes:
        node.start()

    return coordinator, nodes