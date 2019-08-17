import time
from pipelines.state.job_status import status
from datetime import datetime
import logging
import threading

FORMAT = "%(asctime)-15s -function name:%(funcName)s -%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

# TODO: names "compJobClean" and "compJobCleanup" almost the same, what is responsibility??
# TODO: The both actually need to be coupled so that files will get cleaned up when job is kicked out of dict
# TODO: Refactor

def activate_status_cleaning_job():
    def run_job():
        while True:
            for job in status.copy():
                job_time_string = status[job]["timestamp"]
                job_time_obj = datetime.strptime(job_time_string, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()
                delta_time = (current_time - job_time_obj).total_seconds()
                # if job exists more than 30 mins delete it from dictionary
                if delta_time >= 1800.0:
                    status.pop(job)

            time.sleep(30)

    logging.debug("status after loop: " + str(status))
    thread = threading.Thread(target=run_job)
    thread.start()
