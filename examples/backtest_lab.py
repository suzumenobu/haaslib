from haaslib import api
from haaslib.domain import BacktestPeriod
from haaslib.model import CreateLabRequest

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    labs_api = api.LabsAPI(executor)

    # Create a lab (you can also use an existing lab ID)
    lab_details = labs_api.create_lab(
        script_id="your_script_id",
        name="Backtest Example Lab",
        account_id="your_account_id",
        market="BINANCE_BTC_USDT_SPOT",
        interval=15,
        style="CandleStick",
    )
    print(f"Created lab: {lab_details.name}")

    # Run backtest
    start_unix = int(BacktestPeriod(period_type=BacktestPeriod.Type.DAY, count=30).start_unix)
    end_unix = int(BacktestPeriod(period_type=BacktestPeriod.Type.DAY, count=0).end_unix)
    
    labs_api.start_lab_execution(lab_details.lab_id, start_unix, end_unix)
    
    # Wait for execution to complete (you might want to implement a polling mechanism here)
    
    backtest_results = labs_api.get_backtest_result_page(lab_details.lab_id, 0, 1000)

    print(f"Backtest completed. Results:")
    for result in backtest_results:
        print(f"Backtest ID: {result.backtest_id}")
        print(f"Total trades: {result.summary.trades}")
        print(f"Profit: {result.summary.realized_profits}")
        print(f"ROI: {result.summary.return_on_investment}")
        print("---")

if __name__ == "__main__":
    main()