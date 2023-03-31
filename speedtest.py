import os
import subprocess
import re
from logger import get_logger
import datetime
import signal
import time
import sys

_logger = get_logger()

# defining the handler to catch Ctrl-C 
def handler(signum, frame):
    _logger.info("Ctrl-C was pressed, Exiting...")
    sys.exit(0)
signal.signal(signal.SIGINT, handler)

ping = []
down = []
up = []
timestamp = []

while True:
    # run the 'speedtest' command in shell
    output = subprocess.run(['speedtest'], capture_output=True, text=True).stdout

    # regex to find all floats and get the last one
    ping.append(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[4])[-1].strip())
    down.append(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[6])[-1].strip())
    up.append(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", output.split("\n")[8])[-1].strip())
    timestamp.append(datetime.datetime.now())

    _logger.info('ping: {} ms'.format(ping[-1]))
    _logger.info('down: {} Mb/s'.format(down[-1]))
    _logger.info('  up: {} Mb/s'.format(up[-1]))

    time.sleep(10) # 10 seconds