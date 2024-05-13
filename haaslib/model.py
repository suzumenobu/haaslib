from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(alias="Success")
    error: str = Field(alias="Error")
    data: T = Field(alias="Data")


class UserDetails(BaseModel):
    user_id: str = Field(alias="UserId")
    interface_secret: str = Field(alias="UserId")
    license_details: Any = Field(alias="LicenseDetails")


class AppLogin(BaseModel):
    error: int = Field(alias="R")
    details: UserDetails = Field(alias="D")


class HaasBot(BaseModel):
    user_id: str = Field(alias="UI")
    bot_id: str = Field(alias="ID")
    bot_name: str = Field(alias="BN")
    script_id: str = Field(alias="SI")
    script_version: int = Field(alias="SV")
    account_id: str = Field(alias="AI")
    market: str = Field(alias="PM")
    execution_id: str = Field(alias="EI")
    is_activated: bool = Field(alias="IA")
    is_paused: bool = Field(alias="IP")
    is_favorite: bool = Field(alias="IF")
    notes: str = Field(alias="NO")
    script_note: str = Field(alias="SN")
    notes_timestamp: int = Field(alias="NT")
    realized_profit: float = Field(alias="RP")
    urealized_profit: float = Field(alias="UP")
    return_on_investment: float = Field(alias="ROI")
    trade_amount_error: bool = Field(alias="TAE")
    account_error: bool = Field(alias="AE")
    script_error: bool = Field(alias="SE")
    update_counter: int = Field(alias="UC")
    chart_interval: int = Field(alias="CI")
    chart_style: int = Field(alias="CS")
    chart_volume: bool = Field(alias="CV")
    is_white_label: bool = Field(alias="IWL")
    master_bot_id: str = Field(alias="MBID")
    followers: int = Field(alias="F")


class HaasScriptItemWithDependencies(BaseModel):
    dependencies: list[str] = Field(alias="D")
    user_id: str = Field(alias="UID")
    script_id: str = Field(alias="SID")
    script_name: str = Field(alias="SN")
    script_description: str = Field(alias="SD")
    script_type: int = Field(alias="ST")
    script_status: int = Field(alias="SS")
    command_name: str = Field(alias="CN")
    is_command: bool = Field(alias="IC")
    is_valid: bool = Field(alias="IV")
    created_unix: int = Field(alias="CU")
    updated_unix: int = Field(alias="UU")
    folder_id: int = Field(alias="FID")


class CreateLabRequest(BaseModel):
    script_id: str
    name: str
    account_id: str
    market: str
    interval: int
    style: str


class UserAccount(BaseModel):
    user_id: str = Field(alias="UID")
    account_id: str = Field(alias="AID")
    name: str = Field(alias="N")
    exchnage_code: str = Field(alias="EC")
    exchange_type: int = Field(alias="ET")
    status: int = Field(alias="S")
    is_simulated: bool = Field(alias="IS")
    is_test_net: bool = Field(alias="IT")
    is_public: bool = Field(alias="PA")
    is_white_label: bool = Field(alias="WL")
    position_mode: int = Field(alias="PM")
    margin_settings: Any = Field(alias="MS")
    version: int = Field(alias="V")


class UserLabConfig(BaseModel):
    max_population: int = Field(alias="MP")
    max_generations: int = Field(alias="MG")
    max_elites: int = Field(alias="ME")
    mix_rate: float = Field(alias="MR")
    adjust_rate: float = Field(alias="AR")


class ScriptParameters(BaseModel):
    pass


# TODO: Rename all in camelCase
class HaasScriptSettings(BaseModel):
    bot_id: str
    bot_name: str
    account_id: str
    market_tag: str
    position_mode: int
    margin_mode: int
    leverage: float
    trade_amount: float
    interval: int
    chart_style: int
    order_template: int
    script_parameters: ScriptParameters


class UserLabParameterOption(BaseModel):
    value: str | int | float | bool


class UserLabParameter(BaseModel):
    key: str = Field(alias="K")
    input_field_type: int = Field(alias="T")
    options: list[UserLabParameterOption] = Field(alias="O")
    is_enabled: bool = Field(alias="I")
    is_specific: bool = Field(alias="IS")


class UserLabDetails(BaseModel):
    user_lab_config: UserLabConfig = Field(alias="C")
    haas_script_settings: HaasScriptSettings = Field(alias="ST")
    parameters: list[UserLabParameter] = Field(alias="P")
    user_id: str = Field(alias="UID")
    lab_id: str = Field(alias="LID")
    script_id: str = Field(alias="SID")
    name: str = Field(alias="N")
    algorithm: int = Field(alias="T")
    status: int = Field(alias="S")
    scheduled_backtests: int = Field(alias="SB")
    complete_backtests: int = Field(alias="CB")
    created_at: int = Field(alias="CA")
    updated_at: int = Field(alias="UA")
    started_at: int = Field(alias="SA")
    running_since: int = Field(alias="RS")
    start_unix: int = Field(alias="SU")
    end_unix: int = Field(alias="EU")
    send_email: bool = Field(alias="SE")
    cancel_reason: Any = Field(alias="CM")


class StartLabExecutionRequest(BaseModel):
    lab_id: str
    start_unix: int
    end_unix: int
    send_email: bool


class CloudMarket(BaseModel):
    category: str = Field(alias="C")
    price_source: str = Field(alias="PS")
    primary: str = Field(alias="P")
    secondary: str = Field(alias="S")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(alias="I")
    next_page_id: int = Field(alias="NP")


class CustomReportWrapper(BaseModel, Generic[T]):
    data: T = Field(alias="Custom Report")


# FIXME: Write valid field names
class UserLabsBacktestSummary(BaseModel, Generic[T]):
    o: int = Field(alias="O")
    t: int = Field(alias="T")
    p: int = Field(alias="P")
    fc: dict[str, float] = Field(alias="FC")
    rp: dict[str, float] = Field(alias="RP")
    roi: list[float] = Field(alias="ROI")
    custom_report: CustomReportWrapper[T] = Field(alias="CR")


class UserLabBacktestResult(BaseModel):
    record_id: int = Field(alias="RID")
    user_id: str = Field(alias="UID")
    lab_id: str = Field(alias="LID")
    backtest_id: str = Field(alias="BID")
    generation_idx: int = Field(alias="NG")
    population_idx: int = Field(alias="NP")
    status: int = Field(alias="ST")
    settings: HaasScriptSettings = Field(alias="SE")
    parameters: dict[str, str] = Field(alias="P")
    runtime: Any = Field(alias="RT")
    chart: Any = Field(alias="C")
    logs: Any = Field(alias="L")
    summary: UserLabsBacktestSummary = Field(alias="S")


class EditHaasScriptSourceCodeSettings(BaseModel):
    market_tag: CloudMarket
    leverage: float
    position_mode: int
    trade_amount: float
    order_template: int
    chart_style: int
    interval: int
    script_parameters: ScriptParameters
    bot_name: str
    bot_id: str


class CustomReport:
    pass


class GetBacktestResultRequest(BaseModel):
    lab_id: str
    next_page_id: int
    page_lenght: int