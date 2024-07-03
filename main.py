from twisted.internet import reactor

from core.core import main



if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
    