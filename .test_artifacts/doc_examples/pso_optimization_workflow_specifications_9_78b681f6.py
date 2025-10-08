# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 9
# Runnable: False
# Hash: 78b681f6

class PSO_WorkflowOrchestrator:
    """
    Integration point for PSO optimization workflow within multi-agent system.
    """

    def __init__(self, agents: dict):
        self.agents = agents
        self.workflow_manager = OptimizationWorkflowManager()
        self.coordination_protocol = AgentCoordinationProtocol()

    def execute_coordinated_optimization(self, request: OptimizationRequest) -> OrchestrationResult:
        """
        Execute PSO optimization with multi-agent coordination.

        Agent Coordination:
        - Control Systems Specialist: Controller validation and analysis
        - PSO Optimization Engineer: Algorithm tuning and execution
        - Documentation Expert: Process documentation and reporting
        - Integration Coordinator: Cross-domain validation
        """
        result = OrchestrationResult()

        # Phase 1: Pre-optimization coordination
        prep_result = self.coordination_protocol.coordinate_preparation(
            request, self.agents
        )
        if not prep_result.success:
            result.status = 'PREPARATION_FAILED'
            return result

        # Phase 2: Parallel agent execution
        optimization_tasks = {
            'pso_execution': self.agents['pso_engineer'].execute_optimization,
            'controller_validation': self.agents['control_specialist'].validate_controller,
            'documentation': self.agents['documentation_expert'].document_process,
            'integration_check': self.agents['integration_coordinator'].validate_integration
        }

        parallel_results = self.coordination_protocol.execute_parallel_tasks(optimization_tasks)

        # Phase 3: Result integration and validation
        integration_result = self.coordination_protocol.integrate_results(parallel_results)
        result.integration_results = integration_result

        # Phase 4: Quality gate evaluation
        quality_gates = QualityGateSystem(request.config)
        gate_results = quality_gates.evaluate_quality_gates(integration_result)
        result.quality_gate_results = gate_results

        result.status = 'SUCCESS' if gate_results.overall_pass else 'QUALITY_GATE_FAILED'
        return result