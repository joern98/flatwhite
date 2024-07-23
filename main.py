from twisted.internet import reactor

import logging
logging.basicConfig(level=logging.DEBUG, filename="flatwhite_log.txt", filemode='w', format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

from src.core import main

if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
    