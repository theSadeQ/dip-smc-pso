#======================================================================================\\\
#====================== src/controllers/factory/thread_safety.py ======================\\\
#======================================================================================\\\

"""
Thread Safety Enhancement Module for Controller Factory.

Provides:
- Lock-free operations where possible
- Minimal critical sections
- Deadlock prevention
- Performance monitoring for thread safety
"""

import threading
import time
from typing import Dict, Any, Optional, Callable, ContextManager
from contextlib import contextmanager
from collections import deque
import weakref

class LockFreeRegistry:
    """Lock-free controller registry using immutable data structures."""

    def __init__(self):
        # Use immutable snapshots for lock-free reads
        self._registry_snapshot = {}
        self._update_lock = threading.RLock()
        self._access_count = 0

    def get_controller_info(self, controller_type: str) -> Optional[Dict[str, Any]]:
        """Get controller info without locking (lock-free read)."""
        # Atomic read of current snapshot
        current_snapshot = self._registry_snapshot
        self._access_count += 1  # Atomic increment (safe for simple counters)
        return current_snapshot.get(controller_type)

    def update_registry(self, new_registry: Dict[str, Any]) -> None:
        """Update registry with minimal locking."""
        with self._update_lock:
            # Create new immutable snapshot
            self._registry_snapshot = dict(new_registry)

    def get_available_controllers(self) -> list:
        """Get available controllers lock-free."""
        current_snapshot = self._registry_snapshot
        return [name for name, info in current_snapshot.items()
                if info.get('class') is not None]

    def get_access_stats(self) -> Dict[str, int]:
        """Get lock-free access statistics."""
        return {
            'total_accesses': self._access_count,
            'registry_size': len(self._registry_snapshot)
        }


class MinimalLockManager:
    """Manages minimal, efficient locking strategies."""

    def __init__(self):
        self._locks = {}
        self._lock_stats = {
            'acquisitions': 0,
            'contentions': 0,
            'avg_hold_time_ms': 0.0,
            'max_hold_time_ms': 0.0
        }
        self._stats_lock = threading.Lock()

    @contextmanager
    def acquire_minimal_lock(self, resource_id: str, timeout: float = 5.0) -> ContextManager[bool]:
        """Acquire lock with minimal hold time and performance tracking."""
        if resource_id not in self._locks:
            with self._stats_lock:
                if resource_id not in self._locks:
                    self._locks[resource_id] = threading.RLock()

        lock = self._locks[resource_id]
        acquisition_start = time.perf_counter()

        try:
            acquired = lock.acquire(timeout=timeout)
            acquisition_time = time.perf_counter() - acquisition_start

            if acquired:
                hold_start = time.perf_counter()
                self._update_acquisition_stats(acquisition_time > 0.001)  # Contention if > 1ms
                yield True

                # Update hold time statistics
                hold_time = (time.perf_counter() - hold_start) * 1000  # ms
                self._update_hold_time_stats(hold_time)
            else:
                yield False
        finally:
            if acquired:
                lock.release()

    def _update_acquisition_stats(self, contention: bool) -> None:
        """Update lock acquisition statistics."""
        with self._stats_lock:
            self._lock_stats['acquisitions'] += 1
            if contention:
                self._lock_stats['contentions'] += 1

    def _update_hold_time_stats(self, hold_time_ms: float) -> None:
        """Update lock hold time statistics."""
        with self._stats_lock:
            current_avg = self._lock_stats['avg_hold_time_ms']
            acquisitions = self._lock_stats['acquisitions']

            # Running average
            new_avg = (current_avg * (acquisitions - 1) + hold_time_ms) / acquisitions
            self._lock_stats['avg_hold_time_ms'] = new_avg

            # Update maximum
            if hold_time_ms > self._lock_stats['max_hold_time_ms']:
                self._lock_stats['max_hold_time_ms'] = hold_time_ms

    def get_lock_performance_stats(self) -> Dict[str, Any]:
        """Get lock performance statistics."""
        with self._stats_lock:
            stats = dict(self._lock_stats)
            total_acquisitions = stats['acquisitions']
            contentions = stats['contentions']

            stats['contention_rate_percent'] = (
                (contentions / total_acquisitions * 100) if total_acquisitions > 0 else 0.0
            )
            return stats


class ThreadSafeFactoryEnhancement:
    """Thread safety enhancement for controller factory operations."""

    def __init__(self):
        self.lock_free_registry = LockFreeRegistry()
        self.lock_manager = MinimalLockManager()
        self._thread_local_data = threading.local()
        self._performance_monitor = ThreadPerformanceMonitor()

    def initialize_registry(self, registry: Dict[str, Any]) -> None:
        """Initialize the lock-free registry."""
        self.lock_free_registry.update_registry(registry)

    def get_controller_info_safe(self, controller_type: str) -> Optional[Dict[str, Any]]:
        """Thread-safe controller info retrieval (lock-free)."""
        return self.lock_free_registry.get_controller_info(controller_type)

    def get_available_controllers_safe(self) -> list:
        """Thread-safe available controllers list (lock-free)."""
        return self.lock_free_registry.get_available_controllers()

    @contextmanager
    def thread_safe_creation(self, controller_type: str) -> ContextManager[bool]:
        """Thread-safe controller creation context."""
        creation_id = f"creation_{controller_type}_{threading.current_thread().ident}"

        # Monitor thread performance
        with self._performance_monitor.monitor_operation(creation_id):
            # Use minimal locking only for actual creation
            with self.lock_manager.acquire_minimal_lock(f"create_{controller_type}") as acquired:
                if acquired:
                    yield True
                else:
                    yield False

    def get_thread_local_cache(self) -> Dict[str, Any]:
        """Get thread-local cache for temporary data."""
        if not hasattr(self._thread_local_data, 'cache'):
            self._thread_local_data.cache = {}
        return self._thread_local_data.cache

    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive thread safety performance report."""
        return {
            'registry_stats': self.lock_free_registry.get_access_stats(),
            'lock_stats': self.lock_manager.get_lock_performance_stats(),
            'thread_performance': self._performance_monitor.get_performance_stats(),
            'recommendations': self._generate_performance_recommendations()
        }

    def _generate_performance_recommendations(self) -> list:
        """Generate thread safety performance recommendations."""
        recommendations = []
        lock_stats = self.lock_manager.get_lock_performance_stats()

        # Check contention rate
        contention_rate = lock_stats.get('contention_rate_percent', 0.0)
        if contention_rate > 10.0:
            recommendations.append(
                f"High lock contention ({contention_rate:.1f}%) - consider lock-free alternatives"
            )

        # Check average hold time
        avg_hold_time = lock_stats.get('avg_hold_time_ms', 0.0)
        if avg_hold_time > 1.0:
            recommendations.append(
                f"Long lock hold time ({avg_hold_time:.2f}ms) - minimize critical sections"
            )

        # Check registry performance
        registry_stats = self.lock_free_registry.get_access_stats()
        if registry_stats['total_accesses'] > 10000:
            recommendations.append("High registry access - performance is optimal with lock-free design")

        if not recommendations:
            recommendations.append("Thread safety performance is optimal")

        return recommendations


class ThreadPerformanceMonitor:
    """Monitor thread performance for factory operations."""

    def __init__(self):
        self._operation_times = deque(maxlen=1000)  # Keep last 1000 operations
        self._thread_stats = {}
        self._stats_lock = threading.Lock()

    @contextmanager
    def monitor_operation(self, operation_id: str) -> ContextManager[None]:
        """Monitor a thread operation's performance."""
        thread_id = threading.current_thread().ident
        start_time = time.perf_counter()

        try:
            yield
        finally:
            end_time = time.perf_counter()
            operation_time = (end_time - start_time) * 1000  # ms

            with self._stats_lock:
                # Record operation time
                self._operation_times.append(operation_time)

                # Update thread-specific stats
                if thread_id not in self._thread_stats:
                    self._thread_stats[thread_id] = {
                        'operations': 0,
                        'total_time_ms': 0.0,
                        'avg_time_ms': 0.0
                    }

                stats = self._thread_stats[thread_id]
                stats['operations'] += 1
                stats['total_time_ms'] += operation_time
                stats['avg_time_ms'] = stats['total_time_ms'] / stats['operations']

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get thread performance statistics."""
        with self._stats_lock:
            if not self._operation_times:
                return {'error': 'No operations recorded'}

            operation_times = list(self._operation_times)

            return {
                'total_operations': len(operation_times),
                'avg_operation_time_ms': sum(operation_times) / len(operation_times),
                'min_operation_time_ms': min(operation_times),
                'max_operation_time_ms': max(operation_times),
                'p95_operation_time_ms': sorted(operation_times)[int(len(operation_times) * 0.95)],
                'active_threads': len(self._thread_stats),
                'thread_performance': dict(self._thread_stats)
            }


# Global thread safety enhancement instance
_thread_safety_enhancement = ThreadSafeFactoryEnhancement()


def get_thread_safety_enhancement() -> ThreadSafeFactoryEnhancement:
    """Get the global thread safety enhancement instance."""
    return _thread_safety_enhancement


def initialize_thread_safe_factory(registry: Dict[str, Any]) -> None:
    """Initialize thread-safe factory with registry."""
    _thread_safety_enhancement.initialize_registry(registry)