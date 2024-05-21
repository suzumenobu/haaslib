# Table of Contents

1.  [Features](#org1a93f74)
2.  [Usage](#org0526bbe)
3.  [License](#org2bb8985)

Client for [HaasOnline](https://www.haasonline.com) API. Allows automation of Haas trading infrastructure.


<a id="org1a93f74"></a>

# Features

-   API Client handles communication
-   Utilities to create, execute, monitor backtests
-   Classes for key entities like markets, accounts, etc.
-   Custom result handling


<a id="org0526bbe"></a>

# Usage

First of all it required to create `executor` which will interact with API:

    from haaslib import api
    
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())

Guest executor can use some open endpoints, but it's better to authenticate and use all of them:

    executor = executor.authenticate(email="admin@admin.com", password="adm2inadm4in!")

Now it's possible to use all provided endpoint wrappers. Let's create lab and backtest it. Lab requires market, account and script to be created, so they could be acuired in the following way:

    import random
    
    market = random.choice(api.get_all_markets(executor))
    account = random.choice(api.get_accounts(executor))
    script = random.choice(api.get_all_scripts(executor))

Then we can create our lab:

    from haaslib.model import CreateLabRequest
    
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

Now you can see in Haas Web UI (reload page if it was opened already).

To start backtesting `lab` module could be used.

    from haaslib import lab
    from haaslib.domain import BacktestPeriod
    
    backtesting_result = lab.backtest(
        executor,
        lab_details.lab_id,
        BacktestPeriod(period_type=BacktestPeriod.Type.DAY, count=20),
    )

Full example lives in [examples/syncexecutor.py](examples/sync_executor.py) with some other.


<a id="org2bb8985"></a>

# License

This project is licensed under the MIT license.

Let me know if any other sections would be useful to add or if an example should be expanded/clarified! Tried to provide basic overview and configuration to help users get started.

