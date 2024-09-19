from typing import Any

from haaslib.api import SyncExecutor, Authenticated

class UserAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def app_login(self, email: str, secret_key: str) -> Any:
        """
        The 3rd party login.

        :param email: User's email
        :param secret_key: Secret key for authentication
        :return: Login response
        """
        return self.executor.execute(
            endpoint="User",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "APP_LOGIN",
                "email": email,
                "secretkey": secret_key,
            },
        )

    def check_token(self) -> Any:
        """
        This checks if the user login is still valid.

        :return: Token validity status
        """
        return self.executor.execute(
            endpoint="User",
            response_type=Any,  # Replace with a more specific type if known
            query_params={"channel": "CHECK_TOKEN"},
        )

    def logout(self) -> Any:
        """
        Logout procedure.

        :return: Logout response
        """
        return self.executor.execute(
            endpoint="User",
            response_type=Any,  # Replace with a more specific type if known
            query_params={"channel": "LOGOUT"},
        )

    def is_device_approved(self, device_id: str) -> Any:
        """
        Check if a device is approved.

        :param device_id: The ID of the device to check
        :return: Device approval status
        """
        return self.executor.execute(
            endpoint="User",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "IS_DEVICE_APPROVED",
                "deviceid": device_id,
            },
        )