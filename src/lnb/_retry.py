from __future__ import annotations

import random
import time
from typing import Iterator, Optional

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
BASE_DELAY = 0.5  # seconds
MAX_DELAY = 60.0  # seconds


class Attempt:
    """Represents a single request attempt within a retry loop."""

    def __init__(self, number: int, max_retries: int) -> None:
        self.number = number
        self.max_retries = max_retries

    @property
    def is_last(self) -> bool:
        return self.number >= self.max_retries

    def should_retry(self, status_code: int, retry_after: Optional[str]) -> bool:
        """Return True and sleep if we should retry, False otherwise."""
        if self.is_last:
            return False
        if status_code not in RETRYABLE_STATUS_CODES:
            return False
        self._sleep(retry_after)
        return True

    def wait_before_network_retry(self) -> None:
        """Sleep before retrying after a network-level error."""
        self._sleep(None)

    def _sleep(self, retry_after: Optional[str]) -> None:
        if retry_after is not None:
            try:
                delay = float(retry_after)
            except ValueError:
                delay = self._backoff()
        else:
            delay = self._backoff()
        time.sleep(min(delay, MAX_DELAY))

    def _backoff(self) -> float:
        """Exponential backoff with full jitter."""
        cap = BASE_DELAY * (2**self.number)
        return random.uniform(0, min(cap, MAX_DELAY))


class RetryStrategy:
    """Yields Attempt objects for use in a retry loop."""

    def __init__(self, max_retries: int) -> None:
        self.max_retries = max_retries

    def attempts(self) -> Iterator[Attempt]:
        for i in range(self.max_retries + 1):
            yield Attempt(number=i, max_retries=self.max_retries)
