import yaml
import os
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime
import logging
import config
from config import setup_logging
import warnings

warnings.filterwarnings("ignore")

setup_logging()



def sfb_process_11711():
    values_for_11711 = config.values_of_11711