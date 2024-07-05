from haaslib import api


def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="admin@admin.com", password="adm2inadm4in!")

    all_labs = api.get_all_labs(executor)
    print(f"Deleting {len(all_labs)} labs")

    for lab in all_labs:
        api.delete_lab(executor, lab.lab_id)

    print("All labs deleted")


if __name__ == "__main__":
    main()
