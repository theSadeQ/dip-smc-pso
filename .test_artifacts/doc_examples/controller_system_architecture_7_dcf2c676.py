# Example from: docs\architecture\controller_system_architecture.md
# Index: 7
# Runnable: False
# Hash: dcf2c676

# example-metadata:
# runnable: false

class OptimizationPipeline:
    """End-to-end optimization pipeline for SMC controllers."""

    def run_optimization_workflow(
        self,
        controller_type: str,
        base_config: Dict[str, Any],
        optimization_config: Dict[str, Any]
    ) -> OptimizationWorkflowResult:
        """Execute complete optimization workflow."""

        # Phase 1: Preprocessing
        config = self._prepare_optimization_config(base_config, optimization_config)
        bounds = self._get_parameter_bounds(controller_type)

        # Phase 2: PSO Optimization
        optimizer = PSOOptimizer(controller_type, config, config['dynamics'])
        optimization_result = optimizer.optimize(
            n_particles=optimization_config.get('n_particles', 30),
            max_iterations=optimization_config.get('max_iterations', 100),
            convergence_threshold=optimization_config.get('convergence_threshold', 1e-6)
        )

        # Phase 3: Validation
        validation_result = self._validate_optimized_controller(
            controller_type, optimization_result.best_gains, config
        )

        # Phase 4: Result Packaging
        workflow_result = OptimizationWorkflowResult(
            controller_type=controller_type,
            optimization_result=optimization_result,
            validation_result=validation_result,
            optimized_gains=optimization_result.best_gains,
            final_cost=optimization_result.best_cost
        )

        return workflow_result