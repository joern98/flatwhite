from twisted.internet import reactor

from src.core import main

if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
    