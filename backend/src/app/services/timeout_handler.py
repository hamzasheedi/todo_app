"""
Timeout Handler
Implements timeout handling for AI provider requests
"""

import signal
from functools import wraps
from typing import Callable, Any
import logging


logger = logging.getLogger(__name__)


class TimeoutError(Exception):
    """Custom exception for timeout errors"""
    pass


def timeout_handler(timeout_duration: int):
    """
    Decorator to handle timeouts for AI provider requests
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Only works on Unix systems; for cross-platform, we'll use a different approach
            # For now, we'll implement a simple timeout using threading
            import threading
            
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_duration)
            
            if thread.is_alive():
                # Thread is still running, which means timeout occurred
                raise TimeoutError(f"Function {func.__name__} timed out after {timeout_duration} seconds")
            
            if exception[0]:
                raise exception[0]
                
            return result[0]
        
        return wrapper
    return decorator


class TimeoutManager:
    """Manages timeout settings for AI provider requests"""
    
    @staticmethod
    def execute_with_timeout(func: Callable, timeout: int, *args, **kwargs) -> Any:
        """
        Execute a function with a specified timeout
        """
        decorated_func = timeout_handler(timeout)(func)
        return decorated_func(*args, **kwargs)