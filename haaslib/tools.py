import random
from typing import Any, Callable, Optional

from haaslib import api
from haaslib.api import SyncExecutor
from haaslib.model import CloudMarket, HaasBot, BotOrder, BotPosition

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

def find_bot_by_name(bots: list[HaasBot], name: str) -> Optional[HaasBot]:
    """
    Finds a bot by its name in a list of bots.

    :param bots: List of HaasBot objects
    :param name: Name of the bot to find
    :return: HaasBot object if found, None otherwise
    """
    return next((bot for bot in bots if bot.bot_name == name), None)

def calculate_total_position_value(positions: list[BotPosition]) -> float:
    """
    Calculates the total value of all positions.

    :param positions: List of BotPosition objects
    :return: Total value of all positions
    """
    return sum(position.amount * position.current_price for position in positions)

def get_active_orders(orders: list[BotOrder]) -> list[BotOrder]:
    """
    Filters out completed or cancelled orders.

    :param orders: List of BotOrder objects
    :return: List of active BotOrder objects
    """
    return [order for order in orders if order.status not in ["Completed", "Cancelled"]]
