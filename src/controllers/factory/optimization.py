#==========================================================================================\\\
#===================== src/controllers/factory/optimization.py ========================\\\
#==========================================================================================\\\

"""
Factory Optimization Module for Enhanced Performance.

Provides optimizations for:
- Pre-compiled controller configurations
- Cached controller instances
- Lazy loading optimizations
- Reduced instantiation overhead
"""

import time
import threading
from typing import Dict, Any, Optional, Type, Callable
from functools import lru_cache, wraps
import weakref

# Import controller classes for pre-compilation
from ..smc.algorithms.classical.controller import ModularClassicalSMC
from ..smc.algorithms.super_twisting.controller import ModularSuperTwistingSMC
from ..smc.algorithms.adaptive.controller import ModularAdaptiveSMC
from ..smc.algorithms.hybrid.controller import ModularHybridSMC

class ControllerPreCompiler:
    """Pre-compile controller configurations for faster instantiation."""

    def __init__(self):
        self._compiled_configs = {}
        self._lock = threading.RLock()

    @lru_cache(maxsize=128)
    def get_optimized_config(self, controller_type: str, config_hash: str) -> Any:
        """Get pre-compiled controller configuration."""
        # This would contain optimized configuration objects
        # For now, return None to indicate no pre-compilation
        return None

    def precompile_all(self) -> None:
        """Pre-compile all controller configurations."""
        controller_types = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

        for controller_type in controller_types:
            try:
                # Pre-compile default configurations
                self._precompile_default_config(controller_type)
            except Exception as e:
                print(f"Failed to precompile {controller_type}: {e}")

    def _precompile_default_config(self, controller_type: str) -> None:
        """Pre-compile default configuration for a controller type."""
        # Implementation would go here for actual pre-compilation
        pass


class ControllerInstanceCache:
    """Lightweight cache for controller instances with weak references."""

    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self._cache = {}
        self._access_times = {}
        self._lock = threading.RLock()

    def get_cached_instance(self, cache_key: str) -> Optional[Any]:
        """Get cached controller instance if available."""
        with self._lock:
            if cache_key in self._cache:
                # Update access time
                self._access_times[cache_key] = time.time()
                ref = self._cache[cache_key]
                instance = ref() if isinstance(ref, weakref.ref) else ref
                if instance is not None:
                    return instance
                else:
                    # Clean up dead reference
                    del self._cache[cache_key]
                    del self._access_times[cache_key]
            return None

    def cache_instance(self, cache_key: str, instance: Any) -> None:
        """Cache controller instance with weak reference."""
        with self._lock:
            # Cleanup if cache is full
            if len(self._cache) >= self.max_size:
                self._cleanup_old_entries()

            # Store weak reference to avoid memory leaks
            self._cache[cache_key] = weakref.ref(instance)
            self._access_times[cache_key] = time.time()

    def _cleanup_old_entries(self) -> None:
        """Remove oldest entries when cache is full."""
        if not self._access_times:
            return

        # Remove oldest 25% of entries
        sorted_items = sorted(self._access_times.items(), key=lambda x: x[1])
        remove_count = max(1, len(sorted_items) // 4)

        for cache_key, _ in sorted_items[:remove_count]:
            self._cache.pop(cache_key, None)
            self._access_times.pop(cache_key, None)

    def clear(self) -> None:
        """Clear all cached instances."""
        with self._lock:
            self._cache.clear()
            self._access_times.clear()


class FactoryOptimizer:
    """Main factory optimization coordinator."""

    def __init__(self):
        self.precompiler = ControllerPreCompiler()
        self.instance_cache = ControllerInstanceCache()
        self._optimization_enabled = True
        self._performance_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'total_instantiations': 0,
            'avg_instantiation_time_ms': 0.0
        }

    def optimize_instantiation(self, creation_func: Callable) -> Callable:
        """Decorator to optimize controller instantiation."""
        @wraps(creation_func)
        def optimized_creation(*args, **kwargs):
            if not self._optimization_enabled:
                return creation_func(*args, **kwargs)

            start_time = time.perf_counter()

            try:
                # Try cache first (disabled for now as controllers maintain state)
                # cache_key = self._generate_cache_key(*args, **kwargs)
                # cached_instance = self.instance_cache.get_cached_instance(cache_key)
                # if cached_instance is not None:
                #     self._performance_stats['cache_hits'] += 1
                #     return cached_instance

                # Create new instance
                self._performance_stats['cache_misses'] += 1
                instance = creation_func(*args, **kwargs)

                # Cache instance (disabled for stateful controllers)
                # self.instance_cache.cache_instance(cache_key, instance)

                return instance

            finally:
                # Update performance statistics
                end_time = time.perf_counter()
                instantiation_time = (end_time - start_time) * 1000  # ms
                self._update_performance_stats(instantiation_time)

        return optimized_creation

    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate cache key for controller configuration."""
        # For now, disable caching as controllers maintain internal state
        return f"no_cache_{id(args)}_{id(kwargs)}"

    def _update_performance_stats(self, instantiation_time_ms: float) -> None:
        """Update performance statistics."""
        self._performance_stats['total_instantiations'] += 1
        total = self._performance_stats['total_instantiations']
        current_avg = self._performance_stats['avg_instantiation_time_ms']

        # Running average
        new_avg = (current_avg * (total - 1) + instantiation_time_ms) / total
        self._performance_stats['avg_instantiation_time_ms'] = new_avg

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance optimization statistics."""
        total_requests = self._performance_stats['cache_hits'] + self._performance_stats['cache_misses']
        cache_hit_rate = (self._performance_stats['cache_hits'] / total_requests * 100
                         if total_requests > 0 else 0.0)

        return {
            **self._performance_stats,
            'cache_hit_rate_percent': cache_hit_rate,
            'optimization_enabled': self._optimization_enabled
        }

    def enable_optimization(self) -> None:
        """Enable factory optimizations."""
        self._optimization_enabled = True

    def disable_optimization(self) -> None:
        """Disable factory optimizations."""
        self._optimization_enabled = False

    def clear_caches(self) -> None:
        """Clear all caches."""
        self.instance_cache.clear()

    def precompile_configurations(self) -> None:
        """Precompile all controller configurations."""
        self.precompiler.precompile_all()


# Global factory optimizer instance
_factory_optimizer = FactoryOptimizer()


def get_factory_optimizer() -> FactoryOptimizer:
    """Get the global factory optimizer instance."""
    return _factory_optimizer


def optimize_controller_creation(func: Callable) -> Callable:
    """Decorator to optimize controller creation functions."""
    return _factory_optimizer.optimize_instantiation(func)


# Pre-compile configurations on module import
_factory_optimizer.precompile_configurations()