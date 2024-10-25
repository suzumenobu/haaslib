from __future__ import annotations
import time
from collections import deque
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class RateLimiter:
    """Rate limits API requests"""
    requests_per_second: float = 2.0
    
    def __init__(self):
        self.min_interval = 1.0 / self.requests_per_second
        self.last_request_time = 0.0
        self.request_times = deque(maxlen=10)
        self.logger = logger

    def wait(self) -> None:
        """Wait if necessary to maintain rate limit"""
        now = time.time()
        time_since_last = now - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            if sleep_time > 0:
                self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_times.append(self.last_request_time)

    @property
    def requests_in_last_second(self) -> int:
        """Get number of requests made in the last second"""
        now = time.time()
        return sum(1 for t in self.request_times if now - t <= 1.0)
