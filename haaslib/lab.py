"""Lab management functionality for HaasOnline Trading API"""
from __future__ import annotations

import dataclasses
import time
import random
from typing import Generator, Iterable, Sequence, Any
from contextlib import contextmanager

from . import logger
from .api import (
    get_lab_details,
    get_all_markets,
    get_accounts,
    create_lab,
    delete_lab,
    start_lab_execution,
    get_backtest_result,
)
from .executor import Authenticated, RequestsExecutor, HaasApiError
from .model import (
    CreateLabRequest,
    GetBacktestResultRequest,
    StartLabExecutionRequest,
    UserLabBacktestResult,
    UserLabDetails,
    LabSettings,
    UserLabParameter,
    PaginatedResponse,
)

@dataclasses.dataclass
class BacktestPeriod:
    """Represents a backtest time period"""
    start_unix: int
    end_unix: int

@dataclasses.dataclass
class ChangeHaasScriptParameterRequest:
    """Request to change a HaasScript parameter"""
    name: str
    options: list[Any]

class LabError(HaasApiError):
    """Base exception for lab-related errors"""
    pass

class LabManager:
    """Manages lab operations and state"""
    
    def __init__(self, executor: RequestsExecutor[Authenticated]):
        self.executor = executor
        logger.debug(f"Initialized LabManager with executor: {executor}")

    def update_params(
        self,
        settings: Sequence[LabSettings],
        params: Iterable[ChangeHaasScriptParameterRequest],
    ) -> None:
        """Update lab parameters"""
        logger.info("Updating lab parameters")
        try:
            for param in params:
                param_name = param.name.lower()
                setting_idx = next(
                    (i for i, s in enumerate(settings) if param_name in s.bot_name.lower()),
                    None
                )

                if setting_idx is None:
                    raise LabError(f"Failed to find setting for parameter {param.name}")

                settings[setting_idx].script_parameters = param.options
                logger.debug(f"Updated parameter {param.name} with options {param.options}")
        except Exception as e:
            logger.error(f"Error updating parameters: {e}", exc_info=True)
            raise LabError(f"Failed to update parameters: {e}") from e

    def wait_for_execution(self, lab_id: str, timeout: int = 3600) -> None:
        """
        Wait for lab execution to complete
        
        Args:
            lab_id: ID of the lab to monitor
            timeout: Maximum time to wait in seconds (default: 1 hour)
        """
        logger.info(f"Waiting for lab {lab_id} execution to complete")
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise LabError(f"Lab execution timeout after {timeout} seconds")
                
            try:
                details = get_lab_details(self.executor, lab_id)
                if details.status in (2, 3):  # Completed or Cancelled
                    logger.info(f"Lab {lab_id} execution completed with status {details.status}")
                    break
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error checking lab status: {e}", exc_info=True)
                raise LabError(f"Failed to check lab status: {e}") from e

    def backtest(
        self,
        lab_id: str,
        period: BacktestPeriod
    ) -> PaginatedResponse[UserLabBacktestResult]:
        api.start_lab_execution(
            self.executor,
            StartLabExecutionRequest(
                lab_id=lab_id,
                start_unix=period.start_unix,
                end_unix=period.end_unix,
                send_email=False,
            ),
        )

        self.wait_for_execution(lab_id)

        return api.get_backtest_result(
            self.executor,
            GetBacktestResultRequest(lab_id=lab_id, next_page_id=0, page_lenght=1_000_000),
        )

    @contextmanager
    def get_lab_default_params(
        self,
        script_id: str
    ) -> Generator[list[UserLabParameter], None, None]:
        """
        Creates buffer lab to get it's default parameters options

        :param script_id: Script of lab
        """
        accounts = api.get_accounts(self.executor)
        account = random.choice(accounts)

        markets = api.get_all_markets(self.executor)
        market = random.choice(markets)

        req = CreateLabRequest(
            script_id=script_id,
            name="buf_lab",
            account_id=account.account_id,
            market=market.as_market_tag(),
            interval=1,
            default_price_data_style="CandleStick",
        )
        lab_details = api.create_lab(self.executor, req)

        yield lab_details.parameters

        api.delete_lab(self.executor, lab_details.lab_id)
