import time
from haaslib import api
from loguru import logger
import timeit

def main():
    executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
    executor = executor.authenticate(email="garrypotterr@gmail.com", password="IQYTCQJIQYTCQJ")

    all_labs = api.get_all_labs(executor)
    logger.info("Labs to be deleted:")
    for lab in all_labs:
        logger.info(f"- {lab.lab_id} ({lab.name})")
    logger.info(f"\nTotal labs to be deleted: {len(all_labs)}")

    logger.info("\nPress Ctrl+C to cancel, or wait 5 seconds to proceed...")
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        logger.info("\nDeletion cancelled.")
        return

    logger.info("Deleting labs...")
    response_times = []
    freeze_threshold = 5  # seconds
    for lab in all_labs:
        try:
            start_time = timeit.default_timer()
            response = api.delete_lab(executor, lab.lab_id)
            elapsed_time = timeit.default_timer() - start_time
            response_times.append(elapsed_time)
            logger.info(f"Deleted lab {lab.lab_id}: {response} (Time: {elapsed_time:.2f}s)")
            if elapsed_time > freeze_threshold:
                logger.error(f"Potential server freeze detected. Response time exceeded threshold ({freeze_threshold}s).")
                break
            time.sleep(0.5)  # Add a small delay
        except Exception as e:
            logger.error(f"Error deleting lab {lab.lab_id}: {e}")

    if response_times:
        average_response_time = sum(response_times) / len(response_times)
        logger.info(f"\nAverage response time: {average_response_time:.2f}s")

    logger.info("All labs deleted")

if __name__ == "__main__":
    main()
