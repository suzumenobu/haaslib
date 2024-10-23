"""Complete workflow example"""
import time
from datetime import datetime, timedelta

from haaslib import (
    RequestsExecutor,
    Guest,
    LabManager,
    BacktestPeriod,
    CreateLabRequest,
    config,
    logger,
)

def main():
    # Initialize executor
    executor = RequestsExecutor(
        host=config.API_HOST,
        port=config.API_PORT,
        state=Guest(),
        protocol=config.API_PROTOCOL,
        max_retries=3,
        rate_limit_calls=60,
        rate_limit_period=60.0
    )
    
    try:
        # Authenticate
        logger.info("Authenticating...")
        auth_executor = executor.authenticate(
            email=config.API_EMAIL,
            password=config.API_PASSWORD
        )
        
        # Initialize lab manager
        lab_manager = LabManager(auth_executor)
        
        # Get available markets
        markets = auth_executor.get_all_markets()
        logger.info(f"Found {len(markets)} markets")
        
        # Get accounts
        accounts = auth_executor.get_accounts()
        logger.info(f"Found {len(accounts)} accounts")
        
        # Create lab
        lab_details = lab_manager.create_lab(
            CreateLabRequest(
                script_id="your_script_id",
                name="Example Lab",
                account_id=accounts[0].id,
                market=markets[0].as_market_tag(),
                interval=1,
                default_price_data_style="CandleStick"
            )
        )
        logger.info(f"Created lab: {lab_details.lab_id}")
        
        # Run backtest
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        
        backtest_result = lab_manager.backtest(
            lab_details.lab_id,
            BacktestPeriod(
                start_unix=int(start_time.timestamp()),
                end_unix=int(end_time.timestamp())
            )
        )
        
        # Process results
        logger.info(f"Backtest completed with {len(backtest_result.trades)} trades")
        for trade in backtest_result.trades:
            logger.info(
                f"Trade: {trade.side} {trade.amount} @ {trade.price} "
                f"(PnL: {trade.realized_pnl})"
            )
            
    except Exception as e:
        logger.error(f"Error in workflow: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
