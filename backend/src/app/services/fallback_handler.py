"""
Fallback Handler
Implements fallback logic for AI provider failures
"""

import time
from typing import Callable, Any, Optional
from ..config.ai_settings import AISettings
from .ai_provider_factory import AIProviderFactory
import logging


logger = logging.getLogger(__name__)


class FallbackHandler:
    """Handles fallback logic when primary AI provider fails"""
    
    @staticmethod
    def execute_with_fallback(primary_func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with fallback to secondary provider if primary fails
        """
        # Try primary provider first
        try:
            logger.info(f"Attempting to execute with primary provider: {AISettings.AI_PROVIDER}")
            result = primary_func(*args, **kwargs)
            return result
        except Exception as primary_error:
            logger.warning(f"Primary provider failed: {str(primary_error)}")
            
            # Check if fallback is enabled
            if AISettings.FALLBACK_AI_BASE_URL and AISettings.FALLBACK_AI_API_KEY:
                logger.info("Attempting fallback provider...")
                
                try:
                    # Create fallback client and execute function with it
                    fallback_client = AIProviderFactory.create_fallback_client()
                    
                    # Update kwargs to use fallback client if the function expects it
                    if 'client' in kwargs:
                        kwargs['client'] = fallback_client
                    
                    result = primary_func(*args, **kwargs)
                    logger.info("Fallback provider succeeded")
                    return result
                except Exception as fallback_error:
                    logger.error(f"Fallback provider also failed: {str(fallback_error)}")
                    # Raise the original error from primary provider
                    raise primary_error
            else:
                logger.error("No fallback provider configured")
                raise primary_error


class CircuitBreaker:
    """Simple circuit breaker pattern for provider resilience"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call a function with circuit breaker protection"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN - requests blocked")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Called when a call succeeds"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        """Called when a call fails"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return False
        return time.time() - self.last_failure_time >= self.recovery_timeout