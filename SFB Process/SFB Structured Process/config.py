import yaml
import os
from datetime import datetime
import logging

log_folder = ".\\Logs"
os.makedirs(log_folder, exist_ok=True)
log_file = log_folder + "\\SFB_PROCESS_FLOW_" + datetime.now().strftime("%m%d%Y-%H%M%S") + ".log"

# Set up logging configuration
def setup_logging():
    if not logging.getLogger().hasHandlers():  # Avoid re-adding handlers if already configured
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-7s | %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

# ----------------------------------------------------------------------------
config_filepath = "SFB_Config.yaml"

with open(config_filepath, 'r') as file:
    complete_config = yaml.safe_load(file)

RUN_10080 = complete_config['RUN_10080']
RUN_22880 = complete_config['RUN_22880']
RUN_11711 = complete_config['RUN_11711']

values_of_10080 = complete_config['VALUES_10080']
values_of_22880 = complete_config['VALUES_22880']
values_of_11711 = complete_config['VALUES_11711']


