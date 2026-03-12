"""
Test fixture: Custom while-loop retry patterns
Expected: ❌ Issue (first two functions) — manual retry loops without a counter
          ✅ Pass (last function) — manual retry loop with explicit counter

Custom retry loops that don't use a library are subject to the same rule:
a bounded counter must be present.
"""

import time
import requests


# ❌ Pattern 1: while True retry with no counter — runs indefinitely on persistent failure
def fetch_data_no_limit(url: str) -> dict:
    """Fetch data, retrying on failure — no bound on attempts."""
    while True:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            time.sleep(1)
            continue  # back to top of while True with no counter check


# ❌ Pattern 2: for loop retry but no max defined — loop bound is dynamic/external
def call_api_no_max(url: str, retries: int) -> dict:
    """Caller controls retry count — no enforcement at definition site."""
    for _ in range(retries):  # retries comes from caller, could be sys.maxsize
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            time.sleep(0.5)
    raise RuntimeError("All retries exhausted")


# ✅ Pattern 3: while loop with explicit counter and max — bounded
MAX_RETRIES = 3

def fetch_data_with_limit(url: str) -> dict:
    """Fetch data with a hard cap of MAX_RETRIES attempts."""
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            attempt += 1
            if attempt >= MAX_RETRIES:
                raise
            time.sleep(2 ** attempt)  # exponential backoff
    raise RuntimeError("Unreachable")
