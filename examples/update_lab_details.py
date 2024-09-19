import random

from haaslib import api
from haaslib.model import CreateLabRequest


def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    price_api = api.PriceAPI(executor)
    account_api = api.AccountAPI(executor)
    script_api = api.HaasScriptAPI(executor)
    labs_api = api.LabsAPI(executor)

    markets = price_api.market_list()
    market = random.choice(markets)
    print(f"Selected market: {market.name}")

    accounts = account_api.get_accounts()
    account = random.choice(accounts)
    print(f"Selected account: {account.name}")

    scripts = script_api.get_all_script_items()
    script = next(script for script in scripts if script.script_name == "Haasonline Original - Scalper Bot")
    print(f"Selected script: {script.script_name}")

    lab_details = labs_api.create_lab(
        script_id=script.script_id,
        name="Updated Lab Example",
        account_id=account.account_id,
        market=market.name,
        interval=15,
        style="CandleStick",
    )
    print(f"Created lab: {lab_details.name}")

    # Update lab parameters
    lab_details.parameters[0].options = [1, 2, 3, 4, 5]
    updated_lab = labs_api.update_lab_details(
        lab_id=lab_details.lab_id,
        name=lab_details.name,
        type=lab_details.algorithm,
        config=lab_details.user_lab_config,
        settings=lab_details.haas_script_settings,
        parameters=lab_details.parameters,
    )
    print(f"Updated lab: {updated_lab.name}")

if __name__ == "__main__":
    main()
