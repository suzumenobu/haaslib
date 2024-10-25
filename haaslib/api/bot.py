from typing import List, Optional, Dict, Any
from ..executor import RequestsExecutor, Authenticated
from ..models.bot import (
    RuntimeReport,
    AddBotFromLabRequest,
    CreateBotRequest,
    HaasBot,
    HaasBotAndRuntime,
    UserOrder,
    RuntimeOrder,
    OpenPosition,
    ClosedPosition,
)
from ..exceptions import BotError

def get_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> HaasBotAndRuntime:
    """Returns the requested bot with runtime information"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=HaasBotAndRuntime,
        query_params={
            "channel": "GET_BOT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get bot: {response.Error}")
    return response.Data

def get_bots(
    executor: RequestsExecutor[Authenticated]
) -> List[HaasBot]:
    """Returns all the user's bots"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[HaasBot],
        query_params={
            "channel": "GET_BOTS"
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get bots: {response.Error}")
    return response.Data

def add_bot(
    executor: RequestsExecutor[Authenticated],
    request: CreateBotRequest
) -> HaasBot:
    """Creates a new bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=HaasBot,
        query_params={
            "channel": "ADD_BOT",
            "botname": request.bot_name,
            "scriptid": request.script_id,
            "scripttype": request.script_type,
            "accountid": request.account_id,
            "market": request.market,
            "leverage": request.leverage,
            "interval": request.interval,
            "chartstyle": request.chartstyle,
        }
    )
    if not response.Success:
        raise BotError(f"Failed to create bot: {response.Error}")
    return response.Data

def get_runtime_report(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> RuntimeReport:
    """Returns the bot report"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=RuntimeReport,
        query_params={
            "channel": "GET_RUNTIME_REPORT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get runtime report: {response.Error}")
    return response.Data

def get_runtime_open_orders(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> List[UserOrder]:
    """Returns the bot's open orders"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[UserOrder],
        query_params={
            "channel": "GET_RUNTIME_OPEN_ORDERS",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get open orders: {response.Error}")
    return response.Data

def get_open_orders(
    executor: RequestsExecutor[Authenticated]
) -> List[UserOrder]:
    """Returns all open bot orders"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[UserOrder],
        query_params={
            "channel": "GET_OPEN_ORDERS"
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get all open orders: {response.Error}")
    return response.Data

def get_runtime_open_positions(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> List[OpenPosition]:
    """Returns the bot's open positions"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[OpenPosition],
        query_params={
            "channel": "GET_RUNTIME_OPEN_POSITIONS",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get open positions: {response.Error}")
    return response.Data

def get_runtime_closed_positions(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    next_page_id: Optional[str] = None,
    page_length: int = 50
) -> List[ClosedPosition]:
    """Returns the bot's closed positions"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[ClosedPosition],
        query_params={
            "channel": "GET_RUNTIME_CLOSED_POSITIONS",
            "botId": bot_id,
            "nextPageId": next_page_id,
            "pageLength": page_length
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get closed positions: {response.Error}")
    return response.Data

def pause_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> bool:
    """Pauses the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "PAUSE_BOT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to pause bot: {response.Error}")
    return response.Data

def resume_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> bool:
    """Resumes the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "RESUME_BOT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to resume bot: {response.Error}")
    return response.Data

def activate_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> bool:
    """Activates the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "ACTIVATE_BOT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to activate bot: {response.Error}")
    return response.Data

def deactivate_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> bool:
    """Deactivates the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "DEACTIVATE_BOT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to deactivate bot: {response.Error}")
    return response.Data

def delete_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> bool:
    """Deletes the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "DELETE_BOT",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to delete bot: {response.Error}")
    return response.Data

def deactivate_all_bots(
    executor: RequestsExecutor[Authenticated],
    account_id: Optional[str] = None,
    market: Optional[str] = None
) -> bool:
    """Deactivates all bots, optionally filtered by account and market"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "DEACTIVATE_ALL_BOTS",
            "accountId": account_id,
            "market": market
        }
    )
    if not response.Success:
        raise BotError(f"Failed to deactivate all bots: {response.Error}")
    return response.Data

def add_bot_from_backtest(
    executor: RequestsExecutor[Authenticated],
    backtest_id: str,
    bot_name: str,
    account_id: str,
    market: str
) -> HaasBot:
    """Add a new bot from a backtest result"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=HaasBot,
        query_params={
            "channel": "ADD_BOT_FROM_BACKTEST",
            "backtestId": backtest_id,
            "botName": bot_name,
            "accountId": account_id,
            "market": market
        }
    )
    if not response.Success:
        raise BotError(f"Failed to add bot from backtest: {response.Error}")
    return response.Data

def add_bot_from_lab(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    backtest_id: str,
    bot_name: str,
    account_id: str,
    market: str,
    leverage: float = 1.0
) -> HaasBot:
    """Add a new bot from a lab backtest result"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=HaasBot,
        query_params={
            "channel": "ADD_BOT_FROM_LABS",  # Note: matches PHP API's endpoint name
            "labId": lab_id,
            "backtestId": backtest_id,
            "botName": bot_name,
            "accountId": account_id,
            "market": market,
            "leverage": leverage
        }
    )
    if not response.Success:
        raise BotError(f"Failed to add bot from lab: {response.Error}")
    return response.Data

def edit_settings(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    settings: Dict[str, Any]
) -> bool:
    """Edits the bot's settings"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "EDIT_SETTINGS",
            "botId": bot_id,
            "settings": settings
        }
    )
    if not response.Success:
        raise BotError(f"Failed to edit settings: {response.Error}")
    return response.Data

def edit_script(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    script_id: str,
    script_type: str
) -> bool:
    """Edits the bot's script"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "EDIT_SCRIPT",
            "botId": bot_id,
            "scriptId": script_id,
            "scriptType": script_type
        }
    )
    if not response.Success:
        raise BotError(f"Failed to edit script: {response.Error}")
    return response.Data

def rename_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    bot_name: str
) -> bool:
    """Renames the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "RENAME_BOT",
            "botId": bot_id,
            "botName": bot_name
        }
    )
    if not response.Success:
        raise BotError(f"Failed to rename bot: {response.Error}")
    return response.Data

def change_bot_notes(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    notes: str
) -> bool:
    """Changes the notes of/in the bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "CHANGE_BOT_NOTES",
            "botId": bot_id,
            "notes": notes
        }
    )
    if not response.Success:
        raise BotError(f"Failed to change bot notes: {response.Error}")
    return response.Data

def favorite_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    is_favorite: bool
) -> bool:
    """Makes a bot a favorite bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "FAVORITE_BOT",
            "botId": bot_id,
            "isFavorite": is_favorite
        }
    )
    if not response.Success:
        raise BotError(f"Failed to set favorite status: {response.Error}")
    return response.Data

def clone_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    bot_name: str
) -> HaasBot:
    """Clones an existing bot"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=HaasBot,
        query_params={
            "channel": "CLONE_BOT",
            "botId": bot_id,
            "botName": bot_name
        }
    )
    if not response.Success:
        raise BotError(f"Failed to clone bot: {response.Error}")
    return response.Data

def reset_bot(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    config: Dict[str, Any]
) -> bool:
    """Cleans the bot's logbook and trades"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "RESET_BOT",
            "botId": bot_id,
            "config": config
        }
    )
    if not response.Success:
        raise BotError(f"Failed to reset bot: {response.Error}")
    return response.Data

def get_open_positions(
    executor: RequestsExecutor[Authenticated]
) -> List[OpenPosition]:
    """Returns all open bot positions"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[OpenPosition],
        query_params={
            "channel": "GET_OPEN_POSITIONS"
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get open positions: {response.Error}")
    return response.Data

def cancel_order(
    executor: RequestsExecutor[Authenticated],
    bot_id: str,
    order_id: str
) -> bool:
    """Cancels a bot order (manually)"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "CANCEL_ORDER",
            "botId": bot_id,
            "orderId": order_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to cancel order: {response.Error}")
    return response.Data

def cancel_all_orders(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> bool:
    """Cancels all bot orders (manually)"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=bool,
        query_params={
            "channel": "CANCEL_ALL_ORDERS",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to cancel all orders: {response.Error}")
    return response.Data

def get_all_bots(
    executor: RequestsExecutor[Authenticated]
) -> List[HaasBot]:
    """Returns all bots (alias for get_bots)"""
    return get_bots(executor)

def create_bot(
    executor: RequestsExecutor[Authenticated],
    bot_name: str,
    script_id: str,
    script_type: str,
    account_id: str,
    market: str,
    leverage: float = 1.0,
    interval: str = "1m",
    chart_style: str = "CANDLES"
) -> HaasBot:
    """Creates a new bot (alias for add_bot with more descriptive name)"""
    return add_bot(
        executor=executor,
        bot_name=bot_name,
        script_id=script_id,
        script_type=script_type,
        account_id=account_id,
        market=market,
        leverage=leverage,
        interval=interval,
        chart_style=chart_style
    )

def get_bot_status(
    executor: RequestsExecutor[Authenticated],
    bot_id: str
) -> HaasBotAndRuntime:
    """Returns the bot status including runtime information"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=HaasBotAndRuntime,
        query_params={
            "channel": "GET_BOT_STATUS",
            "botId": bot_id
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get bot status: {response.Error}")
    return response.Data

def get_all_scripts(
    executor: RequestsExecutor[Authenticated]
) -> List[Any]:  # TODO: Create proper Script model
    """Returns all available scripts"""
    response = executor.execute(
        endpoint="BotAPI",
        response_type=List[Any],  # TODO: Update when Script model is created
        query_params={
            "channel": "GET_ALL_SCRIPTS"
        }
    )
    if not response.Success:
        raise BotError(f"Failed to get all scripts: {response.Error}")
    return response.Data

# Make sure all functions are exported in __all__
__all__ = [
    'get_bot',
    'get_bots',
    'get_runtime_report',
    'get_runtime_open_orders',
    'get_open_orders',
    'get_runtime_open_positions',
    'get_runtime_closed_positions',
    'add_bot',
    'add_bot_from_lab',
    'add_bot_from_backtest',
    'pause_bot',
    'resume_bot',
    'activate_bot',
    'deactivate_bot',
    'deactivate_all_bots',
    'delete_bot',
    'edit_settings',
    'edit_script',
    'rename_bot',
    'change_bot_notes',
    'favorite_bot',
    'clone_bot',
    'reset_bot',
    'get_open_positions',
    'cancel_order',
    'cancel_all_orders',
    'get_all_bots',
    'create_bot',
    'get_bot_status',
    'get_all_scripts',
]
