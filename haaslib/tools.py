import random
from typing import Any, Callable, Optional

from haaslib import api
from haaslib.api import SyncExecutor
from haaslib.model import CloudMarket


def select_random_markets(
    executor: SyncExecutor[Any],
    count: int,
    filterer: Optional[Callable[[CloudMarket], bool]] = None,
) -> list[CloudMarket]:
    """
    Selects a specified `count` of random markets from a list obtained
    through the Haas API, filtered by a given `filterer`

    :param executor: Executor for Haas API interaction
    :param count: Maxmimum number of markets to return
    :param filterer: Decides which markets should stay (returns `True` for them)
    :raises HaasApiError: If something goes wrong (Not found yet)
    :return: A list of cloud markets that meet the filter criteria,
             randomly selected up to the specified count.
    """
    all_markets = api.get_all_markets(executor)
    if filterer:
        filtered_markets = [m for m in all_markets if filterer(m)]
    else:
        filtered_markets = all_markets

    if count >= len(filtered_markets):
        return filtered_markets

    return random.sample(filtered_markets, count)
