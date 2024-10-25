import unittest
import logging
from ..executor import RequestsExecutor, Guest, Authenticated
from ..exceptions import HaasApiError
from ..models import (
    CloudMarket,
    MarketListResponse,
    UserLabDetails,
    CreateLabRequest
)
from ..api import get_all_markets, get_all_markets_by_pricesource

# Reference to existing test code
