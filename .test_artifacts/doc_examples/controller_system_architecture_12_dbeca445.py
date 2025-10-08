# Example from: docs\architecture\controller_system_architecture.md
# Index: 12
# Runnable: False
# Hash: dbeca445

# example-metadata:
# runnable: false

# Primary Control Flow
def control_loop_data_flow():
    """
    Illustrates the complete data flow through the control system.

    1. Sensor Input → State Vector
    2. State Vector → Controller
    3. Controller → Control Action
    4. Control Action → Plant/Simulator
    5. Plant Response → New State
    6. Loop Continuation with History Updates
    """

    # Step 1: State Acquisition
    current_state = sensor_interface.get_state()  # [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]

    # Step 2: Controller Computation
    control_output = controller.compute_control(
        state=current_state,
        state_vars=previous_state_vars,
        history=control_history
    )

    # Step 3: Control Application
    actuator_command = control_output.control
    plant_response = plant.apply_control(actuator_command, current_state)

    # Step 4: State Update
    next_state = plant_response.next_state

    # Step 5: History Management
    control_history = control_output.history
    previous_state_vars = control_output.state_vars

    # Step 6: Monitoring and Logging
    monitor.log_control_cycle(
        state=current_state,
        control=actuator_command,
        performance=plant_response.performance_metrics
    )

    return next_state, control_history, previous_state_vars