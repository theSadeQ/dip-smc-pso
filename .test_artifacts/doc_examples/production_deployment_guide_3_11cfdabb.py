# Example from: docs\deployment\production_deployment_guide.md
# Index: 3
# Runnable: True
# Hash: 11cfdabb

#!/usr/bin/env python3
"""
Comprehensive health check for SMC controller production deployment.
"""

import os
import sys
import time
import psutil
import requests
import subprocess
from typing import Dict, List, Tuple

class ProductionHealthChecker:
    """Production health monitoring and validation."""

    def __init__(self):
        self.health_checks = [
            self.check_service_status,
            self.check_controller_functionality,
            self.check_system_resources,
            self.check_network_connectivity,
            self.check_disk_space,
            self.check_log_files,
            self.check_configuration,
            self.check_performance_metrics
        ]

    def run_comprehensive_health_check(self) -> Dict[str, bool]:
        """Run all health checks and return results."""

        results = {}
        print("SMC Controller Production Health Check")
        print("=" * 50)

        for check_func in self.health_checks:
            check_name = check_func.__name__.replace('check_', '').replace('_', ' ').title()
            try:
                result = check_func()
                results[check_name] = result
                status = "PASS" if result else "FAIL"
                print(f"{check_name:25} | {status}")
            except Exception as e:
                results[check_name] = False
                print(f"{check_name:25} | FAIL | Error: {str(e)}")

        print("=" * 50)

        # Overall health assessment
        total_checks = len(results)
        passed_checks = sum(results.values())
        health_percentage = (passed_checks / total_checks) * 100

        if health_percentage >= 90:
            overall_status = "EXCELLENT"
        elif health_percentage >= 75:
            overall_status = "GOOD"
        elif health_percentage >= 50:
            overall_status = "WARNING"
        else:
            overall_status = "CRITICAL"

        print(f"Overall Health: {overall_status} ({passed_checks}/{total_checks} checks passed)")
        print(f"Health Score: {health_percentage:.1f}%")

        return results

    def check_service_status(self) -> bool:
        """Check if SMC controller service is running."""
        try:
            result = subprocess.run(['systemctl', 'is-active', 'smc-controller'],
                                  capture_output=True, text=True)
            return result.stdout.strip() == 'active'
        except:
            return False

    def check_controller_functionality(self) -> bool:
        """Check if all controllers are functional."""
        try:
            response = requests.get('http://localhost:8080/health', timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_system_resources(self) -> bool:
        """Check system resource usage."""
        try:
            # CPU usage (average over 1 second)
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Check thresholds
            return cpu_percent < 80 and memory_percent < 85
        except:
            return False

    def check_network_connectivity(self) -> bool:
        """Check network connectivity."""
        try:
            # Check if health endpoint is reachable
            response = requests.get('http://localhost:8080/health', timeout=3)
            return response.status_code == 200
        except:
            return False

    def check_disk_space(self) -> bool:
        """Check available disk space."""
        try:
            # Check main filesystem
            disk_usage = psutil.disk_usage('/')
            free_percent = (disk_usage.free / disk_usage.total) * 100

            # Check logs directory
            logs_usage = psutil.disk_usage('/home/smc-prod/smc-production/logs')
            logs_free_percent = (logs_usage.free / logs_usage.total) * 100

            return free_percent > 10 and logs_free_percent > 5
        except:
            return False

    def check_log_files(self) -> bool:
        """Check log file integrity and recent updates."""
        try:
            log_dir = '/home/smc-prod/smc-production/logs'
            if not os.path.exists(log_dir):
                return False

            # Check if logs are being written (modified within last hour)
            for log_file in os.listdir(log_dir):
                if log_file.endswith('.log'):
                    log_path = os.path.join(log_dir, log_file)
                    mtime = os.path.getmtime(log_path)
                    if time.time() - mtime < 3600:  # 1 hour
                        return True

            return False
        except:
            return False

    def check_configuration(self) -> bool:
        """Check configuration file validity."""
        try:
            config_path = '/home/smc-prod/smc-production/config/production.yaml'

            # Check if config file exists and is readable
            if not os.path.exists(config_path):
                return False

            # Basic YAML syntax check
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Check for required sections
            required_sections = ['simulation', 'physics', 'controllers']
            return all(section in config for section in required_sections)
        except:
            return False

    def check_performance_metrics(self) -> bool:
        """Check if performance metrics are within acceptable ranges."""
        try:
            # This would typically check metrics from Prometheus
            # For now, we'll do a basic performance test

            from src.controllers.factory import create_controller
            import numpy as np

            # Quick performance test
            controller = create_controller('classical_smc')
            state = np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0])

            start_time = time.time()
            for _ in range(100):
                result = controller.compute_control(state)
            elapsed_time = time.time() - start_time

            # Should complete 100 computations in less than 1 second
            return elapsed_time < 1.0
        except:
            return False

if __name__ == "__main__":
    checker = ProductionHealthChecker()
    results = checker.run_comprehensive_health_check()

    # Exit with error code if any critical checks fail
    critical_checks = ['Service Status', 'Controller Functionality', 'System Resources']
    critical_failures = [name for name in critical_checks if not results.get(name, False)]

    if critical_failures:
        print(f"\nCRITICAL FAILURES: {', '.join(critical_failures)}")
        sys.exit(1)
    else:
        print("\nAll critical systems operational")
        sys.exit(0)