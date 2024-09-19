from haaslib import api

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="your_email@example.com", password="your_password")

    script_api = api.HaasScriptAPI(executor)

    # Get all scripts
    all_scripts = script_api.get_all_script_items()
    print(f"Total scripts: {len(all_scripts)}")

    # Create a new script
    new_script = script_api.add_script(
        name="My New Script",
        description="A test script",
        script="// Your script code here",
        script_type=1  # Adjust based on your script types
    )
    print(f"Created new script: {new_script.script_name}")

    # Edit an existing script
    script_api.edit_script(
        script_id=new_script.script_id,
        name="Updated Script Name",
        description="Updated description",
        script="// Updated script code"
    )
    print("Script updated")

    # Delete a script
    script_api.delete_script(new_script.script_id)
    print("Script deleted")

if __name__ == "__main__":
    main()