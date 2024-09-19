from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    
    user_api = api.UserAPI(executor)

    # Perform app login
    login_result = user_api.app_login("your_email@example.com", "your_secret_key")
    print(f"Login successful: {login_result}")

    # Check token validity
    token_valid = user_api.check_token()
    print(f"Token is valid: {token_valid}")

    # Check if a device is approved
    device_id = "your_device_id"
    is_approved = user_api.is_device_approved(device_id)
    print(f"Device {device_id} is approved: {is_approved}")

    # Logout
    logout_result = user_api.logout()
    print(f"Logout successful: {logout_result}")

if __name__ == "__main__":
    main()