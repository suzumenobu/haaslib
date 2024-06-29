import dataclasses
import random
import time
from contextlib import contextmanager
from typing import Generator, Iterable, Sequence

from haaslib import api, iterable_extensions
from haaslib.api import Authenticated, SyncExecutor
from haaslib.domain import BacktestPeriod, MarketTag
from haaslib.model import (
    CreateLabRequest,
    GetBacktestResultRequest,
    PaginatedResponse,
    StartLabExecutionRequest,
    UserLabBacktestResult,
    UserLabParameter,
    UserLabParameterOption,
    UserLabStatus,
)


@dataclasses.dataclass
class ChangeHaasScriptParameterRequest:
    name: str
    options: list[UserLabParameterOption]


def update_params(
    settings: Sequence[UserLabParameter],
    params: Iterable[ChangeHaasScriptParameterRequest],
):
    for param in params:
        param_name = param.name.lower()
        setting_idx = iterable_extensions.find_idx(
            settings, lambda s: param_name in s.key.lower()
        )

        if setting_idx is None:
            raise ValueError(f"Failed to find setting for changer haas script {param=}")

        settings[setting_idx].options = param.options


def wait_for_execution(executor: SyncExecutor[Authenticated], lab_id: str):
    while True:
        details = api.get_lab_details(executor, lab_id)
        match details.status:
            case UserLabStatus.COMPLETED:
                break
            case UserLabStatus.CANCELLED:
                break
            case _:
                pass

        time.sleep(5)


def backtest(
    executor: SyncExecutor[Authenticated], lab_id: str, period: BacktestPeriod
) -> PaginatedResponse[UserLabBacktestResult]:
    api.start_lab_execution(
        executor,
        StartLabExecutionRequest(
            lab_id=lab_id,
            start_unix=period.start_unix,
            end_unix=period.end_unix,
            send_email=False,
        ),
    )

    wait_for_execution(executor, lab_id)

    return api.get_backtest_result(
        executor,
        GetBacktestResultRequest(lab_id=lab_id, next_page_id=0, page_lenght=1_000_000),
    )


@contextmanager
def get_lab_default_params(
    executor: SyncExecutor[Authenticated], script_id: str
) -> Generator[list[UserLabParameter], None, None]:
    """
    Creates buffer lab to get it's default parameters options

    :param executor: Executor for Haas API interaction
    :param script_id: Script of lab
    """
    accounts = api.get_accounts(executor)
    account = random.choice(accounts)

    markets = api.get_all_markets(executor)
    market = random.choice(markets)

    req = CreateLabRequest(
        script_id=script_id,
        name="buf_lab",
        account_id=account.account_id,
        market=market.as_market_tag(),
        interval=1,
        default_price_data_style="CandleStick",
    )
    lab_details = api.create_lab(executor, req)

    yield lab_details.parameters

    api.delete_lab(executor, lab_details.lab_id)
