import sys
from twisted.internet import reactor
import argparse

import logging
parser = argparse.ArgumentParser(prog="flatwhite", usage="flatwhite EPD display application")
parser.add_argument("-l", "--loglevel", default=logging.INFO, choices=logging.getLevelNamesMapping().values(), type=logging.getLevelName)
args = parser.parse_args()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(formatter)
logfile_handler = logging.FileHandler("flatwhite_log.txt", mode="w")
logfile_handler.setFormatter(formatter)
logging.root.addHandler(console_handler)
logging.root.addHandler(logfile_handler)
logging.root.setLevel(args.loglevel)

from src.core import main

if __name__ == "__main__":

    reactor.callWhenRunning(main)
    reactor.run()
    