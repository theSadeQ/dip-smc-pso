# Example from: docs\factory\production_deployment_guide.md
# Index: 3
# Runnable: False
# Hash: 20ac13b5

class ProductionFactoryDeployment:
    """Production deployment manager for factory system."""

    def __init__(self, config):
        self.config = config
        self.current_version = None
        self.new_version = None
        self.rollback_data = {}

    def pre_deployment_checks(self):
        """Run comprehensive pre-deployment validation."""

        checks = {
            'dependencies': self.verify_dependencies(),
            'configuration': self.validate_configuration(),
            'compatibility': self.check_backward_compatibility(),
            'performance': self.benchmark_performance(),
            'health': self.health_check()
        }

        passed = all(checks.values())
        failed_checks = [name for name, result in checks.items() if not result]

        if not passed:
            raise RuntimeError(f"Pre-deployment checks failed: {failed_checks}")

        return checks

    def deploy_with_canary(self, percentage=10):
        """Deploy new factory version using canary strategy."""

        print(f"Starting canary deployment ({percentage}% traffic)")

        # 1. Deploy to canary environment
        canary_success = self.deploy_canary()
        if not canary_success:
            raise RuntimeError("Canary deployment failed")

        # 2. Monitor canary performance
        canary_metrics = self.monitor_canary(duration=300)  # 5 minutes
        if not self.evaluate_canary_metrics(canary_metrics):
            self.rollback_canary()
            raise RuntimeError("Canary metrics below threshold")

        # 3. Gradual rollout
        for percentage in [25, 50, 75, 100]:
            print(f"Rolling out to {percentage}% of traffic")
            self.update_traffic_split(percentage)

            metrics = self.monitor_deployment(duration=180)  # 3 minutes
            if not self.evaluate_metrics(metrics):
                self.rollback_deployment()
                raise RuntimeError(f"Rollout failed at {percentage}%")

        print("✅ Deployment completed successfully")
        return True

    def rollback_deployment(self):
        """Rollback to previous version."""

        print("🔄 Rolling back deployment")

        # Restore previous factory version
        self.restore_factory_version()

        # Verify rollback success
        health_ok = self.health_check()
        if not health_ok:
            raise RuntimeError("Rollback verification failed")

        print("✅ Rollback completed successfully")

# Example deployment
deployment = ProductionFactoryDeployment(production_config)
deployment.pre_deployment_checks()
deployment.deploy_with_canary()