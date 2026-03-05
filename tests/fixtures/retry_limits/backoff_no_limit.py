"""
Test fixture: Backoff decorator without max_tries
Expected: ❌ Issue - Missing retry limit

The backoff library requires max_tries parameter to prevent infinite retries.
"""

import backoff
import requests


# PROBLEMATIC: No max_tries specified
@backoff.on_exception(backoff.expo, requests.RequestException)
def fetch_resource(url: str) -> dict:
    """
    Fetch resource with backoff - PROBLEMATIC.
    
    Uses exponential backoff but has no maximum attempts.
    Will retry forever if the request consistently fails.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


# PROBLEMATIC: Has max_time but no max_tries
@backoff.on_exception(
    backoff.expo,
    requests.RequestException,
    max_time=300,  # 5 minutes max, but could be many attempts
)
def long_poll(endpoint: str) -> dict:
    """
    Long polling with time limit only - PROBLEMATIC.
    
    While max_time provides some bound, the number of attempts
    is still unbounded within that time window.
    """
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()


# PROBLEMATIC: on_predicate without max_tries
@backoff.on_predicate(backoff.fibo, lambda x: x is None)
def wait_for_result(job_id: str) -> dict | None:
    """
    Wait for async result - PROBLEMATIC.
    
    Uses fibonacci backoff but will poll forever until
    the result is non-None.
    """
    return check_job_status(job_id)


def check_job_status(job_id: str) -> dict | None:
    """Check if job is complete."""
    # Simulated job check
    return None  # Would return result when ready
