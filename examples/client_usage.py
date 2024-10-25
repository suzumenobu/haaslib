from haaslib.client import HaasClient
from haaslib.models.lab import CreateLabRequest
from haaslib.domain import BacktestPeriod
from haaslib import logger

def main():
    # Initialize client
    client = HaasClient()
    
    try:
        # Authenticate
        client.authenticate()
        
        # Get available markets
        binance_markets = client.markets.get_markets_by_source("BINANCE")
        logger.info(f"Found {len(binance_markets)} Binance markets")
        
        # Get accounts
        accounts = client.accounts.get_accounts()
        logger.info(f"Found {len(accounts)} accounts")
        
        if accounts and binance_markets:
            # Create a lab
            lab = client.lab.create_new_lab(
                CreateLabRequest(
                    script_id="example_script",
                    name="Test Lab",
                    account_id=accounts[0].account_id,
                    market=binance_markets[0].as_market_tag(),
                    interval=15,
                    default_price_data_style="CandleStick"
                )
            )
            logger.info(f"Created lab: {lab.lab_id}")
            
            # Run backtest
            result = client.lab.run_backtest(
                lab.lab_id,
                BacktestPeriod(
                    period_type=BacktestPeriod.Type.DAY,
                    count=30
                )
            )
            logger.info(f"Backtest completed: {result}")
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
