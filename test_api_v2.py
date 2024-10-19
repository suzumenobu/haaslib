import random
import sys
import traceback

try:
    import requests
except ImportError:
    print("Error: The 'requests' library is not installed. Please install it using 'pip install requests'.")
    sys.exit(1)

try:
    from pydantic import ValidationError
except ImportError:
    print("Error: The 'pydantic' library is not installed. Please install it using 'pip install pydantic'.")
    sys.exit(1)

from haaslib.api import RequestsExecutor, HaasApiError, Guest
from haaslib.model import AuthenticatedSessionResponse

def main():
    try:
        executor = RequestsExecutor(host="127.0.0.1", port=8090, state=Guest())
        try:
            print("Attempting authentication...")
            executor = executor.authenticate(
                email="garrypotterr@gmail.com", password="IQYTCQJIQYTCQJ"
            )
            print("Authentication successful!")
            print(f"Authenticated state: {executor.state}")
        except HaasApiError as e:
            print(f"Authentication failed: {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Exception details:")
            for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
                print(line, end="")
            print("\nAPI Error Details:")
            print(f"Error message: {str(e)}")
        except ValidationError as e:
            print("Validation error occurred:")
            print(e)
            print("\nRaw API response:")
            print(e.json())
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Exception details:")
            for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
                print(line, end="")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure that all required libraries are installed and that the 'haaslib' package is in your Python path.")


if __name__ == "__main__":
    main()
