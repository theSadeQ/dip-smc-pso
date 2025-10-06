#======================================================================================\\\
#===================== src/controllers/factory/core/threading.py ======================\\\
#======================================================================================\\\

"""
Thread-Safe Factory Operations

Provides thread-safe factory operations with timeout protection, deadlock prevention,
and performance monitoring for concurrent controller creation.
"""

import threading
import time
import logging
from typing import Callable, Optional, TypeVar, ParamSpec
from functools import wraps
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Type variables for generic decorator support
P = ParamSpec('P')
T = TypeVar('T')

# =============================================================================
# THREADING INFRASTRUCTURE
# =============================================================================

# Global factory lock with timeout protection
factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds
_DEADLOCK_DETECTION_ENABLED = True

# Performance monitoring
_lock_acquisitions = 0
_lock_contentions = 0
_total_wait_time = 0.0
_max_wait_time = 0.0


class FactoryLockTimeoutError(Exception):
    """Raised when factory lock acquisition times out."""
    pass


class FactoryDeadlockError(Exception):
    """Raised when potential deadlock is detected."""
    pass


# =============================================================================
# THREAD-SAFE DECORATORS
# =============================================================================

def with_factory_lock(
    timeout: Optional[float] = None,
    raise_on_timeout: bool = True
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to make factory functions thread-safe.

    Args:
        timeout: Lock acquisition timeout (default: global timeout)
        raise_on_timeout: Raise exception on timeout vs return None

    Returns:
        Thread-safe decorated function

    Raises:
        FactoryLockTimeoutError: If lock acquisition times out
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            effective_timeout = timeout or _LOCK_TIMEOUT
            start_time = time.perf_counter()

            global _lock_acquisitions, _lock_contentions, _total_wait_time, _max_wait_time

            try:
                # Attempt to acquire lock with timeout
                acquired = factory_lock.acquire(timeout=effective_timeout)

                if not acquired:
                    wait_time = time.perf_counter() - start_time
                    _lock_contentions += 1
                    _total_wait_time += wait_time
                    _max_wait_time = max(_max_wait_time, wait_time)

                    error_msg = (
                        f"Failed to acquire factory lock within {effective_timeout}s for {func.__name__}. "
                        f"Possible deadlock or contention."
                    )
                    logger.error(error_msg)

                    if raise_on_timeout:
                        raise FactoryLockTimeoutError(error_msg)
                    else:
                        return None

                # Track successful acquisition
                wait_time = time.perf_counter() - start_time
                _lock_acquisitions += 1
                _total_wait_time += wait_time
                _max_wait_time = max(_max_wait_time, wait_time)

                if wait_time > 1.0:  # Log slow acquisitions
                    logger.warning(f"Slow lock acquisition for {func.__name__}: {wait_time:.3f}s")

                # Execute the protected function
                return func(*args, **kwargs)

            finally:
                # Always release the lock if we acquired it
                try:
                    if 'acquired' in locals() and acquired:
                        factory_lock.release()
                except RuntimeError:
                    # Lock was not held by current thread - this is a programming error
                    logger.error(f"Attempted to release unheld lock in {func.__name__}")

        return wrapper
    return decorator


@contextmanager
def factory_lock_context(timeout: Optional[float] = None):
    """
    Context manager for thread-safe factory operations.

    Args:
        timeout: Lock acquisition timeout

    Yields:
        None when lock is acquired

    Raises:
        FactoryLockTimeoutError: If lock acquisition times out
    """
    effective_timeout = timeout or _LOCK_TIMEOUT
    start_time = time.perf_counter()

    global _lock_acquisitions, _lock_contentions, _total_wait_time, _max_wait_time

    acquired = False
    try:
        # Attempt to acquire lock with timeout
        acquired = factory_lock.acquire(timeout=effective_timeout)

        if not acquired:
            wait_time = time.perf_counter() - start_time
            _lock_contentions += 1
            _total_wait_time += wait_time
            _max_wait_time = max(_max_wait_time, wait_time)

            error_msg = f"Failed to acquire factory lock within {effective_timeout}s"
            logger.error(error_msg)
            raise FactoryLockTimeoutError(error_msg)

        # Track successful acquisition
        wait_time = time.perf_counter() - start_time
        _lock_acquisitions += 1
        _total_wait_time += wait_time
        _max_wait_time = max(_max_wait_time, wait_time)

        yield

    finally:
        if acquired:
            try:
                factory_lock.release()
            except RuntimeError:
                logger.error("Attempted to release unheld lock in context manager")


# =============================================================================
# DEADLOCK DETECTION AND PREVENTION
# =============================================================================

class DeadlockDetector:
    """Simple deadlock detection based on lock wait times and thread states."""

    def __init__(self, max_wait_time: float = 5.0):
        self.max_wait_time = max_wait_time
        self.waiting_threads = {}
        self.lock = threading.Lock()

    def register_wait(self, thread_id: int, function_name: str) -> None:
        """Register a thread waiting for the factory lock."""
        with self.lock:
            self.waiting_threads[thread_id] = {
                'function': function_name,
                'start_time': time.perf_counter(),
                'thread_name': threading.current_thread().name
            }

    def unregister_wait(self, thread_id: int) -> None:
        """Unregister a thread that has acquired the lock."""
        with self.lock:
            self.waiting_threads.pop(thread_id, None)

    def check_for_deadlock(self) -> Optional[str]:
        """Check for potential deadlock conditions."""
        if not _DEADLOCK_DETECTION_ENABLED:
            return None

        with self.lock:
            current_time = time.perf_counter()
            long_waits = []

            for thread_id, info in self.waiting_threads.items():
                wait_time = current_time - info['start_time']
                if wait_time > self.max_wait_time:
                    long_waits.append({
                        'thread_id': thread_id,
                        'thread_name': info['thread_name'],
                        'function': info['function'],
                        'wait_time': wait_time
                    })

            if len(long_waits) > 1:
                # Multiple threads waiting for extended periods
                details = []
                for wait_info in long_waits:
                    details.append(
                        f"Thread {wait_info['thread_name']} ({wait_info['thread_id']}) "
                        f"waiting {wait_info['wait_time']:.1f}s for {wait_info['function']}"
                    )
                return f"Potential deadlock detected: {'; '.join(details)}"

            return None


# Global deadlock detector
_deadlock_detector = DeadlockDetector()


# =============================================================================
# PERFORMANCE MONITORING AND STATISTICS
# =============================================================================

def get_lock_statistics() -> dict:
    """Get factory lock performance statistics."""
    avg_wait_time = _total_wait_time / max(_lock_acquisitions, 1)
    contention_rate = _lock_contentions / max(_lock_acquisitions, 1)

    return {
        'total_acquisitions': _lock_acquisitions,
        'total_contentions': _lock_contentions,
        'contention_rate': contention_rate,
        'avg_wait_time_ms': avg_wait_time * 1000,
        'max_wait_time_ms': _max_wait_time * 1000,
        'total_wait_time_ms': _total_wait_time * 1000
    }


def reset_lock_statistics() -> None:
    """Reset factory lock performance statistics."""
    global _lock_acquisitions, _lock_contentions, _total_wait_time, _max_wait_time
    _lock_acquisitions = 0
    _lock_contentions = 0
    _total_wait_time = 0.0
    _max_wait_time = 0.0


def enable_deadlock_detection(enabled: bool = True) -> None:
    """Enable or disable deadlock detection."""
    global _DEADLOCK_DETECTION_ENABLED
    _DEADLOCK_DETECTION_ENABLED = enabled
    logger.info(f"Deadlock detection {'enabled' if enabled else 'disabled'}")


def check_thread_safety() -> dict:
    """Check current thread safety status."""
    current_thread = threading.current_thread()

    return {
        'current_thread_id': current_thread.ident,
        'current_thread_name': current_thread.name,
        'lock_held': factory_lock._is_owned(),
        'active_threads': threading.active_count(),
        'deadlock_detection_enabled': _DEADLOCK_DETECTION_ENABLED,
        'potential_deadlock': _deadlock_detector.check_for_deadlock()
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def wait_for_lock_release(timeout: float = 30.0) -> bool:
    """
    Wait for the factory lock to be released by all threads.

    Args:
        timeout: Maximum time to wait

    Returns:
        True if lock was released, False if timeout occurred
    """
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < timeout:
        if not factory_lock._is_owned():
            return True
        time.sleep(0.1)

    return False


def force_unlock() -> bool:
    """
    Force unlock the factory lock (emergency use only).

    Returns:
        True if successfully unlocked, False otherwise

    Warning:
        This is dangerous and should only be used in emergency situations
        where deadlock recovery is necessary.
    """
    try:
        if factory_lock._is_owned():
            # Get the current recursion count
            count = factory_lock._count

            # Release all recursive acquisitions
            for _ in range(count):
                factory_lock.release()

            logger.warning("Factory lock force-unlocked - this may cause race conditions")
            return True
    except Exception as e:
        logger.error(f"Failed to force unlock factory lock: {e}")

    return False