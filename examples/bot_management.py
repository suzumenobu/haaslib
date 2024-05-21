import random

from haaslib import api
from haaslib.model import CreateBotRequest


def main():
    executor = api.RequestsExecutor(
        host="127.0.0.1", port=8090, state=api.Guest()
    ).authenticate(email="admin@admin.com", password="adm2inadm4in!")

    market = random.choice(api.get_all_markets(executor))
    account = random.choice(api.get_accounts(executor))
    script = random.choice(api.get_all_scripts(executor))

    req = CreateBotRequest(
        bot_name="Random configured bot",
        script=script,
        account_id=account.account_id,
        market=market,
    )

    resp = api.add_bot(executor, req)
    print(resp)

    api.delete_bot(executor, resp.bot_id)
    print("Bot deleted")

    bots = api.get_all_bots(executor)
    print(f"Got {len(bots)} bots list: {[bot.bot_name for bot in bots]}")


if __name__ == "__main__":
    main()
