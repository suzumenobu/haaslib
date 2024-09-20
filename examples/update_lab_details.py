import random

from haaslib import api
from haaslib.model import CreateLabRequest


def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())

    markets = api.get_all_markets(executor)
    market = random.choice(markets)
    print(f"Got {len(markets)} and choosed {market}")

    # Authenticate to get access for the all endpoints
    executor = executor.authenticate(
        email="garrypotterr@gmail.com", password="IQYTCQJIQYTCQJ"
    )

    accounts = api.get_accounts(executor)
    account = random.choice(accounts)
    print(f"Got {len(accounts)} and choosed {account}")

    # Get available scripts
    scripts = api.get_all_scripts(executor)
    script = next(
        script
        for script in scripts
        if script.script_name == "Haasonline Original - Scalper Bot"
    )
    print(f"Got {len(scripts)} and choosed {script}")

    # Create lab
    lab_details = api.create_lab(
        executor,
        CreateLabRequest(
            script_id=script.script_id,
            name="My first lab",
            account_id=account.account_id,
            market=market.as_market_tag(),
            interval=0,
            default_price_data_style="CandleStick",
        ),
    )
    print(f"{lab_details=}")
    lab_details.parameters[0].options = [1, 2, 3, 4, 5]
    api.update_lab_details(executor, lab_details)


if __name__ == "__main__":
    main()
