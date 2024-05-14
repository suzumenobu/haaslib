from haaslib import api, lab
from haaslib.domain import BacktestPeriod
from haaslib.logger import log
from haaslib.model import CreateLabRequest


def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())

    # Get markets list
    markets = api.get_all_markets(executor)
    log.info(f"{markets[:5]=}")

    # Authenticate to get access for the all endpoints
    executor = executor.authenticate(email="admin@admin.com", password="adm2inadm4in!")

    # Get accounts list
    accounts = api.get_accounts(executor)
    log.info(f"{accounts=}")

    # Get available scripts
    scripts = api.get_all_scripts(executor)
    log.info(f"{scripts[:5]=}")

    # Create lab
    lab_details = api.create_lab(
        executor,
        CreateLabRequest(
            script_id=scripts[0].script_id,
            name="My first lab",
            account_id=accounts[0].account_id,
            market=markets[0].as_market_tag(),
            interval=0,
            default_price_data_style="CandleStick",
        ),
    )
    log.info(f"{lab_details=}")

    # Start lab backtesting & wait for result
    backtesting_result = lab.backtest(
        executor,
        lab_details.lab_id,
        BacktestPeriod(period_type=BacktestPeriod.Type.DAY, count=20),
    )
    log.info(f"{backtesting_result=}")


if __name__ == "__main__":
    main()
