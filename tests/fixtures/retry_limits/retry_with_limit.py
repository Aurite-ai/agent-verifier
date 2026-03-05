"""
Test fixture: Retry decorator WITH proper max limit
Expected: ✅ Pass - Has explicit retry bounds

This pattern is acceptable because it has explicit stop conditions.
"""

from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential,
    retry_if_exception_type,
)
import requests


# GOOD: Explicit stop_after_attempt
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
def call_api(url: str) -> dict:
    """
    Make API call with bounded retry.
    
    Will attempt at most 3 times before giving up.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


# GOOD: Stop after delay
@retry(
    stop=stop_after_delay(60),  # Max 60 seconds total
    wait=wait_exponential(multiplier=1, min=2, max=30),
)
def long_running_task(task_id: str) -> dict:
    """
    Execute task with time-bounded retry.
    
    Will stop retrying after 60 seconds regardless of attempts.
    """
    return {"task_id": task_id, "status": "completed"}


# GOOD: Combined stop conditions
@retry(
    stop=(stop_after_attempt(5) | stop_after_delay(30)),
    wait=wait_exponential(),
    retry=retry_if_exception_type(requests.RequestException),
)
def robust_api_call(endpoint: str) -> dict:
    """
    API call with multiple safeguards.
    
    Stops after 5 attempts OR 30 seconds, whichever comes first.
    Only retries on network-related exceptions.
    """
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()


# GOOD: Custom retry with explicit counter
def manual_retry_with_limit(func, max_attempts: int = 3):
    """
    Manual retry implementation with explicit limit.
    
    Clear max_attempts parameter makes the bound obvious.
    """
    last_exception = None
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                continue
    raise last_exception
