# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 3
# Runnable: False
# Hash: a4680e2c

# example-metadata:
# runnable: false

class OptimizationWorkflowManager:
    """
    Comprehensive management of PSO optimization workflow execution.
    """

    def __init__(self, config: dict, controller_type: str):
        self.config = config
        self.controller_type = controller_type
        self.monitors = {
            'performance': PerformanceMonitor(),
            'convergence': ConvergenceMonitor(),
            'memory': MemoryMonitor(),
            'safety': SafetyMonitor()
        }
        self.workflow_state = WorkflowState()

    def execute_optimization_workflow(self, controller_factory: Callable) -> OptimizationResult:
        """
        Execute complete PSO optimization workflow with monitoring.

        Workflow Phases:
        1. Pre-optimization setup and validation
        2. PSO tuner initialization
        3. Optimization loop execution
        4. Real-time monitoring and adaptation
        5. Post-optimization validation
        6. Result analysis and reporting
        """
        workflow_start_time = time.time()
        result = OptimizationResult()

        try:
            # Phase 1: Pre-optimization Setup
            setup_result = self._execute_setup_phase(controller_factory)
            result.setup_results = setup_result
            if not setup_result.success:
                result.status = 'SETUP_FAILED'
                return result

            # Phase 2: PSO Tuner Initialization
            tuner_result = self._execute_tuner_initialization()
            result.tuner_results = tuner_result
            if not tuner_result.success:
                result.status = 'TUNER_FAILED'
                return result

            # Phase 3: Optimization Execution
            optimization_result = self._execute_optimization_loop()
            result.optimization_results = optimization_result
            if not optimization_result.success:
                result.status = 'OPTIMIZATION_FAILED'
                return result

            # Phase 4: Post-optimization Validation
            validation_result = self._execute_validation_phase(optimization_result)
            result.validation_results = validation_result

            # Phase 5: Result Analysis
            analysis_result = self._execute_analysis_phase(optimization_result)
            result.analysis_results = analysis_result

            result.status = 'SUCCESS'
            result.total_time = time.time() - workflow_start_time

        except Exception as e:
            result.status = 'ERROR'
            result.error_message = str(e)
            result.total_time = time.time() - workflow_start_time

        return result

    def _execute_setup_phase(self, controller_factory: Callable) -> SetupResult:
        """
        Execute pre-optimization setup and validation.
        """
        setup_result = SetupResult()

        # Validate controller factory
        if not hasattr(controller_factory, 'n_gains'):
            setup_result.errors.append('Controller factory missing n_gains attribute')
            setup_result.success = False
            return setup_result

        # Validate factory functionality
        try:
            test_gains = np.ones(controller_factory.n_gains)
            test_controller = controller_factory(test_gains)
            if not hasattr(test_controller, 'max_force'):
                setup_result.warnings.append('Controller missing max_force attribute')
        except Exception as e:
            setup_result.errors.append(f'Controller factory test failed: {str(e)}')
            setup_result.success = False
            return setup_result

        # Setup monitoring systems
        for name, monitor in self.monitors.items():
            try:
                monitor.initialize(self.config)
                setup_result.monitors_initialized.append(name)
            except Exception as e:
                setup_result.errors.append(f'Monitor {name} initialization failed: {str(e)}')

        # Validate memory availability
        available_memory = psutil.virtual_memory().available / (1024**3)  # GB
        required_memory = self._estimate_memory_requirement()
        if available_memory < required_memory:
            setup_result.warnings.append(f'Low memory: {available_memory:.1f}GB available, {required_memory:.1f}GB recommended')

        setup_result.success = len(setup_result.errors) == 0
        return setup_result

    def _execute_optimization_loop(self) -> OptimizationLoopResult:
        """
        Execute PSO optimization loop with real-time monitoring.
        """
        result = OptimizationLoopResult()

        try:
            # Initialize PSO tuner
            tuner = PSOTuner(
                controller_factory=self.controller_factory,
                config=self.config,
                seed=self.config.get('pso', {}).get('execution', {}).get('seed', 42)
            )

            # Setup optimization monitoring
            optimization_monitor = OptimizationMonitor(
                monitors=self.monitors,
                config=self.config
            )

            # Execute optimization with monitoring
            pso_result = tuner.optimise()

            # Extract results
            result.best_cost = pso_result['best_cost']
            result.best_gains = pso_result['best_pos']
            result.cost_history = pso_result['history']['cost']
            result.position_history = pso_result['history']['pos']

            # Get monitoring data
            result.performance_metrics = optimization_monitor.get_performance_summary()
            result.convergence_analysis = optimization_monitor.get_convergence_analysis()

            result.success = True

        except Exception as e:
            result.success = False
            result.error_message = str(e)

        return result