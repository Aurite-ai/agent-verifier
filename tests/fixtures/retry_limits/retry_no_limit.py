"""
Test fixture: Retry decorator without max limit
Expected: ❌ Issue - Missing retry limit

Retry decorators without explicit limits can cause:
- Infinite retry loops
- Runaway API costs
- Degraded performance
"""

from tenacity import retry, wait_exponential
import requests


# PROBLEMATIC: No stop condition specified
@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def call_api(url: str) -> dict:
    """
    Make API call with retry - PROBLEMATIC.
    
    Uses exponential backoff but has no maximum attempts.
    Will retry forever if the API consistently fails.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


# PROBLEMATIC: Empty retry decorator
@retry
def process_message(message: str) -> str:
    """
    Process message with bare retry - PROBLEMATIC.
    
    No configuration at all means default behavior,
    which may retry indefinitely.
    """
    # Simulated processing that might fail
    if not message:
        raise ValueError("Empty message")
    return message.upper()


# PROBLEMATIC: Only wait specified, no stop
@retry(wait=wait_exponential())
def fetch_data(source: str) -> list:
    """
    Fetch data with exponential backoff - PROBLEMATIC.
    
    Has wait strategy but no stop condition.
    """
    return _internal_fetch(source)


def _internal_fetch(source: str) -> list:
    """Internal fetch implementation."""
    return []
