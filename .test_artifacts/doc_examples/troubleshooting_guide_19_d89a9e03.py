# Example from: docs\factory\troubleshooting_guide.md
# Index: 19
# Runnable: True
# Hash: d89a9e03

import logging
from functools import wraps

def monitor_factory_operations(func):
    """Decorator to monitor factory operations."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('factory_monitor')

        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            duration = (end_time - start_time) * 1000  # ms
            logger.info(f"{func.__name__} completed in {duration:.2f}ms")

            return result

        except Exception as e:
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000

            logger.error(f"{func.__name__} failed after {duration:.2f}ms: {e}")
            raise

    return wrapper

# Apply monitoring to factory functions
import src.controllers.factory as factory
factory.create_controller = monitor_factory_operations(factory.create_controller)