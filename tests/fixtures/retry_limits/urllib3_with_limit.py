"""
Test fixture: urllib3/requests retry with proper total limit
Expected: ✅ Pass — all Retry objects have explicit total= with value > 0

Two valid patterns shown:
1. urllib3.Retry with total and component limits
2. HTTPAdapter receiving an integer directly (also valid)
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ✅ Pattern 1: Retry with explicit total — bounded at 3 attempts
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)


# ✅ Pattern 2: HTTPAdapter with integer max_retries
# An integer value is equivalent to Retry(total=n) — explicitly bounded
adapter2 = HTTPAdapter(max_retries=3)
session2 = requests.Session()
session2.mount("https://", adapter2)


def fetch_with_retry(url: str) -> dict:
    """Fetch a URL with bounded retry logic."""
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
