# getter.py

import subprocess
import re
import datetime
from logger import get_logger

_logger = get_logger()

def get_data():
    # run the 'speedtest' command in shell
    try:
        result = subprocess.run(['speedtest'], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        _logger.error("Speedtest command failed with exit code {}. Error Output: {}".format(e.returncode, e.stderr))
        return [[0, 0, 0, 0]]
    except Exception as e:
        _logger.error("Failed with exception {}".format(e))
        return [[0, 0, 0, 0]]
        
    # regex to find all floats and get the last one for ping, down, and up values
    try:
        ping = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[4])[-1].strip()
        down = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[6])[-1].strip()
        up = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[8])[-1].strip()
        timestamp = datetime.datetime.now()
    
        _logger.info('ping: {} ms'.format(ping))
        _logger.info('down: {} Mb/s'.format(down))
        _logger.info('  up: {} Mb/s'.format(up))
    except IndexError as e:
        _logger.error("Failed to parse speedtest output. IndexError: {}".format(e))
        return None
    except Exception as e:
        _logger.error("Unexpected error occurred while parsing speedtest output: {}".format(e))
        return None

    return [[ping, down, up, timestamp]]
