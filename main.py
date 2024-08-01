import sys
from twisted.internet import reactor
import argparse

import logging

class ColorFormatter(logging.Formatter):
    # Source: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    # Color Reference: https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    cyan = "\x1b[36;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

parser = argparse.ArgumentParser(prog="flatwhite", usage="flatwhite EPD display application")
parser.add_argument("-l", "--loglevel", default=logging.INFO, choices=logging.getLevelNamesMapping().values(), type=logging.getLevelName)
args = parser.parse_args()

color_formatter = ColorFormatter()
basic_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s")
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(color_formatter)
logfile_handler = logging.FileHandler("flatwhite_log.txt", mode="w")
logfile_handler.setFormatter(basic_formatter)
logging.root.addHandler(console_handler)
logging.root.addHandler(logfile_handler)
logging.root.setLevel(args.loglevel)

from src.core import main

if __name__ == "__main__":

    reactor.callWhenRunning(main)
    reactor.run()
    