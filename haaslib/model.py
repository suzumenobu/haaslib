import enum
from typing import Any, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, Field

from haaslib.domain import MarketTag

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(alias="Success")
    error: str = Field(alias="Error")
    data: Optional[T] = Field(alias="Data")


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


PriceDataStyle = Literal[
    "CandleStick",
    "CandleStickHLC",
    "HeikinAshi",
    "OHLC",
    "HLC",
    "CloseLine",
    "Line",
    "Mountain",
]


class CreateLabRequest(BaseModel):
    script_id: str
    name: str
    account_id: str
    market: MarketTag
    interval: int
    default_price_data_style: PriceDataStyle


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


class HaasScriptSettings(BaseModel):
    bot_id: str = Field(alias="botId")
    bot_name: str = Field(alias="botName")
    account_id: str = Field(alias="accountId")
    market_tag: str = Field(alias="marketTag")
    position_mode: int = Field(alias="positionMode")
    margin_mode: int = Field(alias="marginMode")
    leverage: float = Field(alias="leverage")
    trade_amount: float = Field(alias="tradeAmount")
    interval: int = Field(alias="interval")
    chart_style: int = Field(alias="chartStyle")
    order_template: int = Field(alias="orderTemplate")
    script_parameters: ScriptParameters = Field(alias="scriptParameters")


class UserLabParameterOption(BaseModel):
    value: str | int | float | bool


class UserLabParameter(BaseModel):
    key: str = Field(alias="K")
    input_field_type: int = Field(alias="T")
    options: list[UserLabParameterOption] = Field(alias="O")
    is_enabled: bool = Field(alias="I")
    is_specific: bool = Field(alias="IS")


class UserLabStatus(enum.Enum):
    CREATED = 0
    QUEUED = 1
    RUNNING = 2
    COMPLETED = 3
    CANCELLED = 4


class UserLabDetails(BaseModel):
    user_lab_config: UserLabConfig = Field(alias="C")
    haas_script_settings: HaasScriptSettings = Field(alias="ST")
    parameters: list[UserLabParameter] = Field(alias="P")
    user_id: str = Field(alias="UID")
    lab_id: str = Field(alias="LID")
    script_id: str = Field(alias="SID")
    name: str = Field(alias="N")
    algorithm: int = Field(alias="T")
    status: UserLabStatus = Field(alias="S")
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


class UserLabRecord(BaseModel):
    user_id: str = Field(alias="UID")
    lab_id: str = Field(alias="LID")
    script_id: str = Field(alias="SID")
    name: str = Field(alias="N")
    scheduled_backtests: int = Field(alias="SB")
    completed_backtests: int = Field(alias="CB")
    created_at: int = Field(alias="CA")
    updated_at: int = Field(alias="UA")
    started_at: int = Field(alias="SA")
    running_since: int = Field(alias="RS")
    start_unix: int = Field(alias="SU")
    end_unix: int = Field(alias="EU")
    send_email: bool = Field(alias="SE")
    cancel_reason: str = Field(alias="CM")


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

    def as_market_tag(self) -> MarketTag:
        return MarketTag(
            f"{self.price_source}_{self.primary}_{self.secondary}_{self.category}"
        )


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(alias="I")
    next_page_id: int = Field(alias="NP")


class CustomReportWrapper(BaseModel, Generic[T]):
    data: Optional[T] = Field(alias="Custom Report", default=None)


class UserLabsBacktestSummary(BaseModel, Generic[T]):
    orders: int = Field(alias="O")
    trades: int = Field(alias="T")
    positions: int = Field(alias="P")
    fee_costs: dict[str, float] = Field(alias="FC")
    realized_profits: dict[str, float] = Field(alias="RP")
    return_on_investment: list[float] = Field(alias="ROI")
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


class LicenseDetails(BaseModel):
    generated: int = Field(alias="Generated")
    license_name: str = Field(alias="LicenseName")
    valid_until: int = Field(alias="ValidUntill")
    rights: int = Field(alias="Rights")
    enterprise: bool = Field(alias="Enterprise")
    allowed_exchanges: list = Field(alias="AllowedExchanges")
    max_bots: int = Field(alias="MaxBots")
    max_simulated_accounts: int = Field(alias="MaxSimulatedAccounts")
    max_real_accounts: int = Field(alias="MaxRealAccounts")
    max_dashboards: int = Field(alias="MaxDashboards")
    max_backtest_months: int = Field(alias="MaxBacktestMonths")
    max_labs_months: int = Field(alias="MaxLabsMonths")
    max_open_orders: int = Field(alias="MaxOpenOrders")
    rented_signals: dict[str, Any] = Field(alias="RentedSignals")
    rented_strategies: dict[str, Any] = Field(alias="RentedStrategies")
    hire_signals_enabled: bool = Field(alias="HireSignalsEnabled")
    hire_strategies_enabled: bool = Field(alias="HireStrategiesEnabled")
    haas_labs_enabled: bool = Field(alias="HaasLabsEnabled")
    resell_signals_enabled: bool = Field(alias="ResellSignalsEnabled")
    market_details_enabled: bool = Field(alias="MarketDetailsEnabled")
    local_api_enabled: bool = Field(alias="LocalAPIEnabled")
    scripted_exchanges_enabled: bool = Field(alias="ScriptedExchangesEnabled")
    machine_learning_enabled: bool = Field(alias="MachinelearningEnabled")


class AuthenticatedSessionResponseData(BaseModel):
    user_id: str = Field(alias="UserId")
    username: Any = Field(alias="Username")
    interface_secret: str = Field(alias="InterfaceSecret")
    user_rights: int = Field(alias="UserRights")
    is_affiliate: bool = Field(alias="IsAffiliate")
    is_product_seller: bool = Field(alias="IsProductSeller")
    license_details: LicenseDetails = Field(alias="LicenseDetails")
    support_hash: Any = Field(alias="SupportHash")


class AuthenticatedSessionResponse(BaseModel):
    data: AuthenticatedSessionResponseData = Field(alias="D")
