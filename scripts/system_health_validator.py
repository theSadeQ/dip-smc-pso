#==========================================================================================\\\
#================================ scripts/system_health_validator.py =====================\\\
#==========================================================================================\\\
"""
System Health Validation Matrix Framework for DIP-SMC-PSO Project.

This module provides comprehensive system health validation across all domains
with a focus on integration readiness and production deployment validation.
"""

import json
import sys
import subprocess
import time
import importlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HealthComponent:
    """Individual health component assessment."""
    name: str
    status: str  # 'healthy', 'warning', 'critical', 'unknown'
    score: float  # 0.0 to 1.0
    details: Dict[str, Any]
    recommendations: List[str]


@dataclass
class SystemHealthReport:
    """Comprehensive system health validation report."""
    overall_score: float
    overall_status: str
    components: Dict[str, HealthComponent]
    integration_score: float
    production_readiness: float
    blocking_issues: List[str]
    timestamp: str
    validation_matrix: Dict[str, bool]


class SystemHealthValidator:
    """Comprehensive system health validation matrix."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.src_dir = self.project_root / "src"
        self.test_dir = self.project_root / "tests"

    def validate_controller_domain(self) -> HealthComponent:
        """Validate controller domain health."""
        details = {}
        recommendations = []
        score = 0.0

        try:
            # Check controller factory availability
            controller_factory = self.src_dir / "controllers" / "factory.py"
            if controller_factory.exists():
                score += 0.3
                details['factory_exists'] = True
            else:
                recommendations.append("Create controller factory")

            # Check core controllers
            core_controllers = [
                "classic_smc.py", "sta_smc.py", "adaptive_smc.py",
                "hybrid_adaptive_sta_smc.py", "swing_up_smc.py"
            ]

            controllers_dir = self.src_dir / "controllers"
            existing_controllers = []
            if controllers_dir.exists():
                for controller in core_controllers:
                    if (controllers_dir / controller).exists():
                        existing_controllers.append(controller)
                        score += 0.1

            details['controllers_available'] = existing_controllers
            details['controller_count'] = len(existing_controllers)

            # Check test coverage for controllers
            controller_tests_dir = self.test_dir / "test_controllers"
            if controller_tests_dir.exists():
                test_files = list(controller_tests_dir.rglob("test_*.py"))
                details['controller_tests'] = len(test_files)
                if len(test_files) >= 10:
                    score += 0.2
                elif len(test_files) >= 5:
                    score += 0.1
            else:
                recommendations.append("Create controller test directory")

            # Determine status
            if score >= 0.8:
                status = 'healthy'
            elif score >= 0.6:
                status = 'warning'
            else:
                status = 'critical'

        except Exception as e:
            status = 'unknown'
            details['error'] = str(e)
            recommendations.append(f"Fix controller domain error: {e}")

        return HealthComponent(
            name="Controller Domain",
            status=status,
            score=score,
            details=details,
            recommendations=recommendations
        )

    def validate_optimization_domain(self) -> HealthComponent:
        """Validate optimization domain health."""
        details = {}
        recommendations = []
        score = 0.0

        try:
            # Check PSO optimizer
            pso_file = self.src_dir / "optimizer" / "pso_optimizer.py"
            if pso_file.exists():
                score += 0.4
                details['pso_optimizer_exists'] = True
            else:
                recommendations.append("Create PSO optimizer")

            # Check optimization test coverage
            opt_tests_dir = self.test_dir / "test_optimization"
            if opt_tests_dir.exists():
                test_files = list(opt_tests_dir.rglob("test_*.py"))
                details['optimization_tests'] = len(test_files)
                if len(test_files) >= 5:
                    score += 0.3
                elif len(test_files) >= 2:
                    score += 0.1
            else:
                recommendations.append("Create optimization test directory")

            # Check critical dependencies
            try:
                import numpy
                import scipy
                score += 0.2
                details['critical_deps_available'] = True
            except ImportError:
                recommendations.append("Install numpy/scipy dependencies")

            # Check Numba for performance optimization
            try:
                import numba
                score += 0.1
                details['numba_available'] = True
            except ImportError:
                recommendations.append("Install numba for optimization")

            # Determine status
            if score >= 0.8:
                status = 'healthy'
            elif score >= 0.6:
                status = 'warning'
            else:
                status = 'critical'

        except Exception as e:
            status = 'unknown'
            details['error'] = str(e)
            recommendations.append(f"Fix optimization domain error: {e}")

        return HealthComponent(
            name="Optimization Domain",
            status=status,
            score=score,
            details=details,
            recommendations=recommendations
        )

    def validate_testing_infrastructure(self) -> HealthComponent:
        """Validate testing infrastructure health."""
        details = {}
        recommendations = []
        score = 0.0

        try:
            # Check pytest availability
            try:
                import pytest
                score += 0.2
                details['pytest_available'] = True
            except ImportError:
                recommendations.append("Install pytest")

            # Check test collection
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Parse test count
                lines = result.stdout.split('\n')
                for line in lines:
                    if "tests collected" in line:
                        try:
                            test_count = int(line.split()[0])
                            details['tests_collected'] = test_count
                            if test_count >= 1000:
                                score += 0.3
                            elif test_count >= 500:
                                score += 0.2
                            elif test_count >= 100:
                                score += 0.1
                            break
                        except (ValueError, IndexError):
                            continue
            else:
                recommendations.append("Fix test collection errors")

            # Check conftest.py files
            conftest_files = list(self.project_root.rglob("conftest.py"))
            details['conftest_files'] = len(conftest_files)
            if conftest_files:
                score += 0.1

            # Check test structure
            if self.test_dir.exists():
                test_files = list(self.test_dir.rglob("test_*.py"))
                details['test_files'] = len(test_files)
                if len(test_files) >= 100:
                    score += 0.2
                elif len(test_files) >= 50:
                    score += 0.1
            else:
                recommendations.append("Create test directory structure")

            # Check hypothesis for property-based testing
            try:
                import hypothesis
                score += 0.1
                details['hypothesis_available'] = True
            except ImportError:
                recommendations.append("Install hypothesis for property-based testing")

            # Determine status
            if score >= 0.8:
                status = 'healthy'
            elif score >= 0.6:
                status = 'warning'
            else:
                status = 'critical'

        except Exception as e:
            status = 'unknown'
            details['error'] = str(e)
            recommendations.append(f"Fix testing infrastructure error: {e}")

        return HealthComponent(
            name="Testing Infrastructure",
            status=status,
            score=score,
            details=details,
            recommendations=recommendations
        )

    def validate_configuration_domain(self) -> HealthComponent:
        """Validate configuration domain health."""
        details = {}
        recommendations = []
        score = 0.0

        try:
            # Check main config file
            config_file = self.project_root / "config.yaml"
            if config_file.exists():
                score += 0.3
                details['main_config_exists'] = True
            else:
                recommendations.append("Create main config.yaml file")

            # Check config module
            config_module = self.src_dir / "config.py"
            if config_module.exists():
                score += 0.2
                details['config_module_exists'] = True
            else:
                recommendations.append("Create config module")

            # Check config validation
            config_tests = self.test_dir / "test_config"
            if config_tests.exists():
                test_files = list(config_tests.rglob("test_*.py"))
                details['config_tests'] = len(test_files)
                if len(test_files) >= 3:
                    score += 0.2
                elif len(test_files) >= 1:
                    score += 0.1
            else:
                recommendations.append("Create config validation tests")

            # Check Pydantic for validation
            try:
                import pydantic
                score += 0.2
                details['pydantic_available'] = True
            except ImportError:
                recommendations.append("Install pydantic for config validation")

            # Check YAML support
            try:
                import yaml
                score += 0.1
                details['yaml_support'] = True
            except ImportError:
                recommendations.append("Install PyYAML for config support")

            # Determine status
            if score >= 0.8:
                status = 'healthy'
            elif score >= 0.6:
                status = 'warning'
            else:
                status = 'critical'

        except Exception as e:
            status = 'unknown'
            details['error'] = str(e)
            recommendations.append(f"Fix configuration domain error: {e}")

        return HealthComponent(
            name="Configuration Domain",
            status=status,
            score=score,
            details=details,
            recommendations=recommendations
        )

    def validate_analysis_domain(self) -> HealthComponent:
        """Validate analysis domain health."""
        details = {}
        recommendations = []
        score = 0.0

        try:
            # Check analysis utilities
            analysis_dir = self.src_dir / "utils" / "analysis"
            if analysis_dir.exists():
                analysis_files = list(analysis_dir.glob("*.py"))
                details['analysis_modules'] = len(analysis_files)
                if len(analysis_files) >= 3:
                    score += 0.2
                elif len(analysis_files) >= 1:
                    score += 0.1
            else:
                recommendations.append("Create analysis utilities")

            # Check visualization support
            viz_dir = self.src_dir / "utils" / "visualization"
            if viz_dir.exists():
                viz_files = list(viz_dir.glob("*.py"))
                details['visualization_modules'] = len(viz_files)
                if len(viz_files) >= 2:
                    score += 0.2
                elif len(viz_files) >= 1:
                    score += 0.1

            # Check matplotlib availability
            try:
                import matplotlib
                score += 0.2
                details['matplotlib_available'] = True
            except ImportError:
                recommendations.append("Install matplotlib for visualization")

            # Check analysis tests
            analysis_tests = self.test_dir / "test_analysis"
            if analysis_tests.exists():
                test_files = list(analysis_tests.rglob("test_*.py"))
                details['analysis_tests'] = len(test_files)
                if len(test_files) >= 5:
                    score += 0.3
                elif len(test_files) >= 2:
                    score += 0.1
            else:
                recommendations.append("Create analysis test suite")

            # Check statistical analysis
            try:
                import scipy.stats
                score += 0.1
                details['scipy_stats_available'] = True
            except ImportError:
                recommendations.append("Install scipy for statistical analysis")

            # Determine status
            if score >= 0.8:
                status = 'healthy'
            elif score >= 0.6:
                status = 'warning'
            else:
                status = 'critical'

        except Exception as e:
            status = 'unknown'
            details['error'] = str(e)
            recommendations.append(f"Fix analysis domain error: {e}")

        return HealthComponent(
            name="Analysis Domain",
            status=status,
            score=score,
            details=details,
            recommendations=recommendations
        )

    def validate_integration_readiness(self) -> Tuple[float, List[str]]:
        """Validate cross-domain integration readiness."""
        integration_score = 0.0
        blocking_issues = []

        try:
            # Check import structure
            critical_modules = [
                "src.controllers.factory",
                "src.optimizer.pso_optimizer",
                "src.config"
            ]

            importable_modules = 0
            for module in critical_modules:
                try:
                    importlib.import_module(module)
                    importable_modules += 1
                except ImportError as e:
                    blocking_issues.append(f"Cannot import {module}: {e}")

            integration_score += (importable_modules / len(critical_modules)) * 0.4

            # Check interface compatibility
            if (self.src_dir / "controllers" / "factory.py").exists():
                integration_score += 0.2

            # Check configuration loading
            if (self.project_root / "config.yaml").exists():
                integration_score += 0.2

            # Check test integration
            if (self.test_dir / "test_integration").exists():
                integration_score += 0.2

        except Exception as e:
            blocking_issues.append(f"Integration validation error: {e}")

        return integration_score, blocking_issues

    def calculate_production_readiness(self, components: Dict[str, HealthComponent]) -> float:
        """Calculate overall production readiness score."""
        weights = {
            'Controller Domain': 0.25,
            'Optimization Domain': 0.20,
            'Testing Infrastructure': 0.25,
            'Configuration Domain': 0.15,
            'Analysis Domain': 0.15
        }

        weighted_score = 0.0
        for name, component in components.items():
            weight = weights.get(name, 0.0)
            weighted_score += component.score * weight

        return weighted_score

    def create_validation_matrix(self, components: Dict[str, HealthComponent]) -> Dict[str, bool]:
        """Create validation matrix for go/no-go decisions."""
        matrix = {}

        for name, component in components.items():
            matrix[f"{name.lower().replace(' ', '_')}_healthy"] = component.status in ['healthy', 'warning']
            matrix[f"{name.lower().replace(' ', '_')}_score_acceptable"] = component.score >= 0.5

        # Overall validation checks
        matrix['all_components_importable'] = all(
            'error' not in comp.details for comp in components.values()
        )

        matrix['critical_tests_passing'] = components.get('Testing Infrastructure', HealthComponent(
            '', 'unknown', 0.0, {}, []
        )).score >= 0.6

        return matrix

    def run_comprehensive_health_check(self) -> SystemHealthReport:
        """Run comprehensive system health validation."""
        logger.info("Starting comprehensive system health validation...")

        # Validate all domains
        components = {
            'Controller Domain': self.validate_controller_domain(),
            'Optimization Domain': self.validate_optimization_domain(),
            'Testing Infrastructure': self.validate_testing_infrastructure(),
            'Configuration Domain': self.validate_configuration_domain(),
            'Analysis Domain': self.validate_analysis_domain()
        }

        # Calculate integration readiness
        integration_score, blocking_issues = self.validate_integration_readiness()

        # Calculate production readiness
        production_readiness = self.calculate_production_readiness(components)

        # Calculate overall score
        overall_score = sum(comp.score for comp in components.values()) / len(components)

        # Determine overall status
        if overall_score >= 0.8 and len(blocking_issues) == 0:
            overall_status = 'healthy'
        elif overall_score >= 0.6:
            overall_status = 'warning'
        else:
            overall_status = 'critical'

        # Create validation matrix
        validation_matrix = self.create_validation_matrix(components)

        report = SystemHealthReport(
            overall_score=overall_score,
            overall_status=overall_status,
            components=components,
            integration_score=integration_score,
            production_readiness=production_readiness,
            blocking_issues=blocking_issues,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            validation_matrix=validation_matrix
        )

        logger.info(f"Health validation complete. Overall score: {overall_score:.2f}")
        return report


def main():
    """Main entry point for system health validation."""
    validator = SystemHealthValidator()
    report = validator.run_comprehensive_health_check()

    # Save report
    report_path = Path("validation") / "system_health_validation_report.json"
    report_path.parent.mkdir(exist_ok=True)

    # Convert HealthComponent objects to dictionaries for JSON serialization
    serializable_report = asdict(report)

    with open(report_path, 'w') as f:
        json.dump(serializable_report, f, indent=2)

    print(f"\nSystem Health Validation Report")
    print(f"{'='*50}")
    print(f"Overall Score: {report.overall_score:.2f}/1.0")
    print(f"Overall Status: {report.overall_status.upper()}")
    print(f"Integration Score: {report.integration_score:.2f}/1.0")
    print(f"Production Readiness: {report.production_readiness:.2f}/1.0")
    print(f"Blocking Issues: {len(report.blocking_issues)}")

    print(f"\nComponent Health:")
    for name, component in report.components.items():
        print(f"  {name}: {component.score:.2f} ({component.status})")

    if report.blocking_issues:
        print(f"\nBlocking Issues:")
        for issue in report.blocking_issues:
            print(f"  - {issue}")

    print(f"\nValidation Matrix (Passing: {sum(report.validation_matrix.values())}/{len(report.validation_matrix)}):")
    for check, result in report.validation_matrix.items():
        status = "PASS" if result else "FAIL"
        print(f"  {check}: {status}")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()