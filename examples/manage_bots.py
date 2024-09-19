from haaslib import api
from haaslib.model import CreateBotRequest

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    bot_api = api.BotAPI(executor)
    price_api = api.PriceAPI(executor)
    script_api = api.HaasScriptAPI(executor)

    # Create a bot
    new_bot = bot_api.add_bot(
        bot_name="Example Bot",
        script_id=script_api.get_all_script_items()[0].script_id,
        account_id="your_account_id",
        market=price_api.market_list()[0].name,
        leverage=1,
        interval=15,
        chartstyle=301,
    )
    print(f"Created bot: {new_bot.bot_name}")

    # Get all bots
    all_bots = bot_api.get_bots()
    print(f"Total bots: {len(all_bots)}")

    # Activate a bot
    bot_api.activate_bot(new_bot.bot_id)
    print(f"Activated bot: {new_bot.bot_name}")

    # Get bot details
    bot_details = bot_api.get_bot(new_bot.bot_id)
    print(f"Bot details: {bot_details}")

    # Deactivate a bot
    bot_api.deactivate_bot(new_bot.bot_id)
    print(f"Deactivated bot: {new_bot.bot_name}")

    # Delete a bot
    bot_api.delete_bot(new_bot.bot_id)
    print(f"Deleted bot: {new_bot.bot_name}")

if __name__ == "__main__":
    main()