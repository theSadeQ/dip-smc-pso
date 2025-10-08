# Example from: docs\reference\interfaces\hil_fault_injection.md
# Index: 3
# Runnable: True
# Hash: cf58cd67

from src.interfaces.hil.fault_injection import FaultInjector, FaultType

# Packet loss fault
injector = FaultInjector()

injector.add_fault(
    fault_type=FaultType.PACKET_LOSS,
    loss_probability=0.2,  # 20% packet loss
    start_time=3.0,
    duration=5.0
)

# HIL with communication faults
for t in np.arange(0, 10, 0.01):
    # Request state from server
    state_msg = client.request_state()

    # Apply packet loss
    if injector.check_packet_loss(t):
        # Use last known state
        state = last_state
    else:
        state = state_msg.state

    control = controller.compute(state)
    client.send_control(control)
    last_state = state