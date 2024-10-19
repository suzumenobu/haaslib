import os
import subprocess

def main():
    try:
        host = os.environ["HAAS_HOST"]
        port = int(os.environ["HAAS_PORT"])
        email = os.environ["HAAS_EMAIL"]
        password = os.environ["HAAS_PASSWORD"]

        command = [
            "python",
            "delete_all_labs.py",
            f"--host={host}",
            f"--port={port}",
            f"--email={email}",
            f"--password={password}",
        ]
        subprocess.run(command, check=True)
    except KeyError as e:
        print(f"Missing environment variable: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error running delete_all_labs.py: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
