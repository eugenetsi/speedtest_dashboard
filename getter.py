# getter.py

import subprocess
import re
import datetime
from logger import get_logger

_logger = get_logger()

def get_data():
    # run the 'speedtest' command in shell
    try:
        output = subprocess.run(['speedtest'], capture_output=True, text=True).stdout
    except Exception as e:
        _logger.error("Failed with exception {}".format(e))

    # regex to find all floats and get the last one
    ping = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[4])[-1].strip()
    down = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[6])[-1].strip()
    up = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[8])[-1].strip()
    timestamp = datetime.datetime.now()

    _logger.info('ping: {} ms'.format(ping))
    _logger.info('down: {} Mb/s'.format(down))
    _logger.info('  up: {} Mb/s'.format(up))

    return [[ping, down, up, timestamp]]