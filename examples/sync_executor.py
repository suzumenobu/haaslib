from src import api


def main():
    executor = api.RequestsExecutor(address="", port=0, protocol="", state=api.Guest())
    api.get_all_markets(executor)

    authenticated = executor.authenticate()
    api.get_accounts(authenticated)


if __name__ == "__main__":
    pass
