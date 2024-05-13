import dataclasses
import time
from typing import Iterable, Sequence

from haaslib import api, iterable_extensions
from haaslib.api import Authenticated, SyncExecutor
from haaslib.domain import BacktestPeriod
from haaslib.model import (
    GetBacktestResultRequest,
    PaginatedResponse,
    StartLabExecutionRequest,
    UserLabBacktestResult,
    UserLabParameter,
    UserLabParameterOption,
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
            case 1:
                break
            case 2:
                break
            case _:
                pass
        time.sleep(5)


def execute(
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
