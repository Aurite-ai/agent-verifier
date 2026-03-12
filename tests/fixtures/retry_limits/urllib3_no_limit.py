"""
Test fixture: urllib3/requests retry without total limit
Expected: ❌ Issue — Retry objects missing required `total=` parameter

Three patterns that should all be flagged:
1. urllib3.Retry with no total
2. urllib3.Retry with total=0 (explicitly disables retries)
3. HTTPAdapter receiving a Retry object that has no total
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ❌ Pattern 1: Retry with no total — will use urllib3 default of 10
retry_strategy = Retry(
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)


# ❌ Pattern 2: Retry with total=0 — explicitly disables all retries
retry_no_retries = Retry(
    total=0,
    raise_on_status=False,
)
adapter2 = HTTPAdapter(max_retries=retry_no_retries)


# ❌ Pattern 3: Retry specifying connect= and read= but not total
# connect= and read= do not bound the total number of retries
retry_partial = Retry(
    connect=3,
    read=3,
    backoff_factor=0.3,
)
adapter3 = HTTPAdapter(max_retries=retry_partial)
