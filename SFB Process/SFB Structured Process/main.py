import config
import warnings
import logging
from config import setup_logging
from BU_10080 import sfb_process_10080
from BU_22880 import sfb_process_22880
from BU_11711 import sfb_process_11711


warnings.filterwarnings("ignore")

setup_logging()
try:
    logging.info("SFB PROCESS STARTED !!!")
    logging.info("-" * 30)

    run_10080 = config.RUN_10080
    if(run_10080):
        logging.info("Executing the process for 10080")
        sfb_process_10080()
        logging.info("Process Successfully completed for 10080.")
        logging.info()

    run_22880 = config.RUN_22880
    if(run_22880):
        logging.info("Executing the process for 22880")
        sfb_process_22880()
        logging.info("Process Successfully completed for 10080.")
        logging.info()

    run_11711 = config.RUN_11711
    if(run_11711):
        logging.info("Executing the process for 11711")
        sfb_process_11711()
        logging.info("Process Successfully completed for 11711.")
        


    logging.info("-" * 30)
    logging.info("SFB PROCESS COMPLETED !!!")

except Exception as err:
    logging.error(f"An unexpected error Occured: {err}")