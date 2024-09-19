from typing import Any

from haaslib.api import SyncExecutor, Authenticated

class SignalAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def store_signal(self, id: str, secret: str, signal: Any) -> Any:
        """
        Use this webhook to send signals to the HaasCloud.

        :param id: The signal ID
        :param secret: The secret key
        :param signal: The signal data
        :return: Response from the API
        """
        return self.executor.execute(
            endpoint="Signal",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "STORE_SIGNAL",
                "id": id,
                "secret": secret,
                "signal": signal,
            },
        )

    def my_signals(self) -> Any:
        """
        This returns a list of all the user's signals.

        :return: List of user's signals
        """
        return self.executor.execute(
            endpoint="Signal",
            response_type=Any,  # Replace with a more specific type if known
            query_params={"channel": "MY_SIGNALS"},
        )