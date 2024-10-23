import dataclasses
import time
from typing import Generator, Iterable, Sequence

from .api import get_lab_details
from .executor import Authenticated, RequestsExecutor
from .model import (
    CreateLabRequest,
    GetBacktestResultRequest,
    UserLabBacktestResult,
    UserLabDetails,
    LabSettings,
)


@dataclasses.dataclass
class ChangeHaasScriptParameterRequest:
    name: str
    options: list[Any]  # Replace with proper type when available


def update_params(
    settings: Sequence[LabSettings],
    params: Iterable[ChangeHaasScriptParameterRequest],
):
    for param in params:
        param_name = param.name.lower()
        setting_idx = next(
            (i for i, s in enumerate(settings) if param_name in s.bot_name.lower()),
            None
        )

        if setting_idx is None:
            raise ValueError(f"Failed to find setting for parameter {param.name}")

        settings[setting_idx].script_parameters = param.options


def wait_for_execution(executor: RequestsExecutor[Authenticated], lab_id: str):
    while True:
        details = get_lab_details(executor, lab_id)
        if details.status in (2, 3):  # Completed or Cancelled
            break
        time.sleep(5)


def backtest(
    executor: RequestsExecutor[Authenticated], lab_id: str, period: BacktestPeriod
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
    executor: RequestsExecutor[Authenticated], script_id: str
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

