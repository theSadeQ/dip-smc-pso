# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 18
# Runnable: False
# Hash: 07011719

# example-metadata:
# runnable: false

import logging
import logging.handlers
from pathlib import Path
import gzip
import os
from datetime import datetime, timedelta

class PSOLogManager:
    """Centralized PSO log management."""

    def __init__(self, log_directory='./logs', max_log_size_mb=100, backup_count=10):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.max_log_size = max_log_size_mb * 1024 * 1024  # Convert to bytes
        self.backup_count = backup_count

        self._setup_loggers()

    def _setup_loggers(self):
        """Setup rotating file handlers for different log types."""

        # PSO optimization logs
        pso_handler = logging.handlers.RotatingFileHandler(
            self.log_directory / 'pso_optimization.log',
            maxBytes=self.max_log_size,
            backupCount=self.backup_count
        )
        pso_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        ))

        self.pso_logger = logging.getLogger('pso_optimization')
        self.pso_logger.addHandler(pso_handler)
        self.pso_logger.setLevel(logging.INFO)

        # System health logs
        health_handler = logging.handlers.RotatingFileHandler(
            self.log_directory / 'system_health.log',
            maxBytes=self.max_log_size,
            backupCount=self.backup_count
        )
        health_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))

        self.health_logger = logging.getLogger('system_health')
        self.health_logger.addHandler(health_handler)
        self.health_logger.setLevel(logging.INFO)

    def log_optimization_start(self, controller_type, config):
        """Log optimization start."""
        self.pso_logger.info(f"Starting PSO optimization for {controller_type}")
        self.pso_logger.info(f"PSO config: particles={config.get('n_particles')}, iterations={config.get('n_iterations')}")

    def log_optimization_result(self, controller_type, results):
        """Log optimization results."""
        success = results.get('success', False)
        best_cost = results.get('best_cost', 'unknown')
        convergence_iter = results.get('convergence_iteration', 'unknown')

        self.pso_logger.info(f"PSO optimization for {controller_type} completed: success={success}")
        self.pso_logger.info(f"Best cost: {best_cost}, Convergence iteration: {convergence_iter}")

        if not success:
            self.pso_logger.warning(f"PSO optimization failed for {controller_type}")

    def log_health_check(self, health_status, issues):
        """Log system health check results."""
        self.health_logger.info(f"Health check completed: status={health_status}")

        if issues:
            for issue in issues:
                self.health_logger.warning(f"Health issue: {issue}")

    def cleanup_old_logs(self, days_to_keep=30):
        """Clean up old log files."""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for log_file in self.log_directory.glob('*.log*'):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                # Compress old logs before deletion
                if not log_file.name.endswith('.gz'):
                    compressed_name = f"{log_file}.gz"
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_name, 'wb') as f_out:
                            f_out.writelines(f_in)
                    os.remove(log_file)
                    self.health_logger.info(f"Compressed and archived log: {log_file}")

    def get_log_summary(self, days=7):
        """Get summary of recent log activity."""
        summary = {
            'optimization_runs': 0,
            'successful_optimizations': 0,
            'health_checks': 0,
            'warnings': 0,
            'errors': 0
        }

        cutoff_date = datetime.now() - timedelta(days=days)

        # Analyze PSO logs
        pso_log_file = self.log_directory / 'pso_optimization.log'
        if pso_log_file.exists():
            with open(pso_log_file, 'r') as f:
                for line in f:
                    # Parse log lines and count events
                    if 'Starting PSO optimization' in line:
                        summary['optimization_runs'] += 1
                    elif 'completed: success=True' in line:
                        summary['successful_optimizations'] += 1
                    elif 'WARNING' in line:
                        summary['warnings'] += 1
                    elif 'ERROR' in line:
                        summary['errors'] += 1

        # Analyze health logs
        health_log_file = self.log_directory / 'system_health.log'
        if health_log_file.exists():
            with open(health_log_file, 'r') as f:
                for line in f:
                    if 'Health check completed' in line:
                        summary['health_checks'] += 1

        return summary

# Usage
log_manager = PSOLogManager()

# Log optimization session
log_manager.log_optimization_start('classical_smc', {'n_particles': 50, 'n_iterations': 100})
# ... run optimization ...
log_manager.log_optimization_result('classical_smc', {'success': True, 'best_cost': 67.3})

# Daily maintenance
log_manager.cleanup_old_logs(days_to_keep=30)
summary = log_manager.get_log_summary(days=7)
print(f"Last 7 days: {summary['optimization_runs']} optimizations, {summary['successful_optimizations']} successful")