import argparse
import sys
import os
from haaslib.api import (
    create_lab,
    update_lab_details,
    delete_lab,
    add_bot,
    delete_bot,
    get_all_labs,
    get_all_bots,
    get_lab_details,
    HaasApiError,
    get_all_markets,
)
from haaslib.model import (
    CreateLabRequest,
    UserLabDetails,
    HaasBot,
    CreateBotRequest,
    AddBotFromLabRequest,
    CloudMarket,
    MarketTag,
    Script,
    HaasScriptItemWithDependencies,
    UserAccount,
    PriceDataStyle,
)
import requests
import json

def main():
    parser = argparse.ArgumentParser(description="Return API responses for HaasOnline commands.")
    parser.add_argument("command", choices=["create_lab", "update_lab", "delete_lab", "add_bot", "delete_bot", "get_labs", "get_bots", "get_lab_details", "get_markets"], help="API command to execute.")
    parser.add_argument("--lab_id", help="ID of the lab (required for update, delete, and get_lab_details).")
    parser.add_argument("--bot_id", help="ID of the bot (required for delete).")
    parser.add_argument("--name", help="Name of the lab (required for create_lab).")
    parser.add_argument("--details", help="Details of the lab (required for update_lab), JSON string.")
    parser.add_argument("--bot_name", help="Name of the bot (required for add_bot).")
    parser.add_argument("--bot_details", help="Details of the bot (required for add_bot), JSON string.")
    parser.add_argument("--script_id", help="Script ID (required for add_bot and create_lab).")
    parser.add_argument("--account_id", help="Account ID (required for add_bot and create_lab).")
    parser.add_argument("--market", help="Market (required for add_bot and create_lab).")
    parser.add_argument("--interval", type=int, default=15, help="Interval (required for add_bot and create_lab).")
    parser.add_argument("--default_price_data_style", default="CandleStick", help="Default price data style (required for add_bot and create_lab).")
    parser.add_argument("--backtest_id", help="Backtest ID (required for add_bot).")
    parser.add_argument("--leverage", type=int, default=0, help="Leverage (optional for add_bot).")
    parser.add_argument("--chartstyle", type=int, default=301, help="Chart style (optional for add_bot).")
    parser.add_argument("--script_type", type=int, help="Script type (required for add_bot).")


    args = parser.parse_args()

    try:
        if args.command == "create_lab":
            if not args.name or not args.script_id or not args.account_id or not args.market or not args.default_price_data_style:
                raise ValueError("Name, script_id, account_id, market, and default_price_data_style are required for create_lab.")
            market_tag = MarketTag(args.market)
            response = create_lab(CreateLabRequest(script_id=args.script_id, name=args.name, account_id=args.account_id, market=market_tag, interval=args.interval, default_price_data_style=PriceDataStyle(args.default_price_data_style)))
            print(response.json())
        elif args.command == "update_lab":
            if not args.lab_id or not args.details:
                raise ValueError("lab_id and details are required for update_lab.")
            try:
                details_dict = json.loads(args.details)
                response = update_lab_details(args.lab_id, UserLabDetails(**details_dict))
                print(response.json())
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error in details: {e}", file=sys.stderr)
        elif args.command == "delete_lab":
            if not args.lab_id:
                raise ValueError("lab_id is required for delete_lab.")
            response = delete_lab(args.lab_id)
            print(response.json())
        elif args.command == "add_bot":
            if not args.bot_name or not args.bot_details or not args.script_id or not args.account_id or not args.market or not args.default_price_data_style or not args.backtest_id or not args.lab_id or not args.script_type:
                raise ValueError("bot_name, bot_details, script_id, account_id, market, default_price_data_style, backtest_id, lab_id, and script_type are required for add_bot.")
            try:
                market_tag = MarketTag(args.market)
                bot_details_dict = json.loads(args.bot_details)
                script = HaasScriptItemWithDependencies(script_id=args.script_id, type=args.script_type)
                response = add_bot(CreateBotRequest(bot_name=args.bot_name, script=script, account_id=args.account_id, market=market_tag, interval=args.interval, chartstyle=args.chartstyle))
                print(response.json())
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error in bot_details: {e}", file=sys.stderr)
        elif args.command == "delete_bot":
            if not args.bot_id:
                raise ValueError("bot_id is required for delete_bot.")
            response = delete_bot(args.bot_id)
            print(response.json())
        elif args.command == "get_labs":
            response = get_all_labs()
            print(response.json())
        elif args.command == "get_bots":
            response = get_all_bots()
            print(response.json())
        elif args.command == "get_lab_details":
            if not args.lab_id:
                raise ValueError("lab_id is required for get_lab_details.")
            response = get_lab_details(args.lab_id)
            print(response.json())
        elif args.command == "get_markets":
            response = get_all_markets()
            print(response.json())
        else:
            raise ValueError("Invalid command.")

    except HaasApiError as e:
        print(f"API Error: {e}", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
