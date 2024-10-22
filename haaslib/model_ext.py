from typing import List, Any, Optional
from pydantic import BaseModel, Field

class AccountData(BaseModel):
    balances: List[Any] = Field(alias="Balances")
    orders: List[Any] = Field(alias="Orders")
    positions: List[Any] = Field(alias="Positions")
    trades: List[Any] = Field(alias="Trades")

class AccountBalance(BaseModel):
    account_id: str = Field(alias="AccountId")
    balance: float = Field(alias="Balance")
    currency: str = Field(alias="Currency")

class AccountOrder(BaseModel):
    account_id: str = Field(alias="AccountId")
    order_id: str = Field(alias="OrderId")
    # Add other fields as needed

class AccountPosition(BaseModel):
    account_id: str = Field(alias="AccountId")
    position_id: str = Field(alias="PositionId")
    # Add other fields as needed

class AccountTrade(BaseModel):
    account_id: str = Field(alias="AccountId")
    trade_id: str = Field(alias="TradeId")
    # Add other fields as needed

class LabConfig(BaseModel):
    max_population: int = Field(alias="MP")
    max_generations: int = Field(alias="MG")
    max_elites: int = Field(alias="ME")
    mix_rate: float = Field(alias="MR")
    adjust_rate: float = Field(alias="AR")


class LabSettings(BaseModel):
    bot_id: Optional[str] = Field(alias="botId")
    bot_name: Optional[str] = Field(alias="botName")
    account_id: Optional[str] = Field(alias="accountId")
    market_tag: Optional[str] = Field(alias="marketTag")
    position_mode: int = Field(alias="positionMode")
    margin_mode: int = Field(alias="marginMode")
    leverage: float = Field(alias="leverage")
    trade_amount: float = Field(alias="tradeAmount")
    interval: int = Field(alias="interval")
    chart_style: int = Field(alias="chartStyle")
    order_template: int = Field(alias="orderTemplate")
    script_parameters: Any = Field(alias="scriptParameters")


class LabParameter(BaseModel):
    key: str = Field(alias="K")
    input_field_type: int = Field(alias="T")
    options: List[Any] = Field(alias="O")
    is_enabled: bool = Field(alias="I")
    is_specific: bool = Field(alias="IS")


class LabExecutionUpdate(BaseModel):
    status: int = Field(alias="S")
    progress: int = Field(alias="P")
    message: str = Field(alias="M")

class BacktestResult(BaseModel):
    pass

class CloudMarket(BaseModel):
    price_source: str = Field(alias="PriceSource")
    primary: str = Field(alias="Primary")
    secondary: str = Field(alias="Secondary")
    contract_name: str = Field(alias="ContractName")
    short_name: str = Field(alias="ShortName")
    wallet_tag: str = Field(alias="WalletTag")

class CloudTradeMarket(BaseModel):
    normalized_primary: str = Field(alias="NormalizedPrimary")
    normalized_secondary: str = Field(alias="NormalizedSecondary")
    normalized_margin_currency: str = Field(alias="NormalizedMarginCurrency")
    exchange_symbol: str = Field(alias="ExchangeSymbol")
    web_socket_symbol: str = Field(alias="WebSocketSymbol")
    exchange_value: float = Field(alias="ExchangeValue")
    exchange_values: List[float] = Field(alias="ExchangeValues")
    price_step: float = Field(alias="PriceStep")
    price_decimals: int = Field(alias="PriceDecimals")
    amount_step: float = Field(alias="AmountStep")
    amount_decimals: int = Field(alias="AmountDecimals")
    price_decimal_type: str = Field(alias="PriceDecimalType")
    amount_decimal_type: str = Field(alias="AmountDecimalType")
    makers_fee: float = Field(alias="MakersFee")
    takers_fee: float = Field(alias="TakersFee")
    minimum_trade_amount: float = Field(alias="MinimumTradeAmount")
    minimum_trade_volume: float = Field(alias="MinimumTradeVolume")
    is_open: bool = Field(alias="IsOpen")
    is_margin: bool = Field(alias="IsMargin")
    contract_details: Any = Field(alias="ContractDetails")
    margin_currency: str = Field(alias="MarginCurrency")
    amount_label: str = Field(alias="AmountLabel")
    profit_label: str = Field(alias="ProfitLabel")
    price_source: str = Field(alias="PriceSource")
    primary: str = Field(alias="Primary")
    secondary: str = Field(alias="Secondary")
    contract_name: str = Field(alias="ContractName")
    short_name: str = Field(alias="ShortName")
    wallet_tag: str = Field(alias="WalletTag")
