import logging
import sys
from threading import Thread, current_thread
import time
from twisted.internet import reactor
from io import StringIO


class Observable:

    def __init__(self) -> None:
        self.__observers = []

    def subscribe(self, callback):
        self.__observers.append(callback)
        
    def unsubscribe(self, callback):
        self.__observers.remove(callback)

    def notify(self):
        for f in self.__observers:
            f()

KEY1_PRESSED = Observable()
KEY2_PRESSED = Observable()
KEY3_PRESSED = Observable()
KEY4_PRESSED = Observable()

KEY1_PRESSED.subscribe(lambda: logging.info("KEY1 pressed!"))
KEY2_PRESSED.subscribe(lambda: logging.info("KEY2 pressed!"))
KEY3_PRESSED.subscribe(lambda: logging.info("KEY3 pressed!"))
KEY4_PRESSED.subscribe(lambda: logging.info("KEY4 pressed!"))

try:
    from gpiozero import Button

    __PIN_KEY1 = 5
    __PIN_KEY2 = 6
    __PIN_KEY3 = 13
    __PIN_KEY4 = 19 

    __BUTTON_KEY1 = Button(__PIN_KEY1)
    __BUTTON_KEY2 = Button(__PIN_KEY2)
    __BUTTON_KEY3 = Button(__PIN_KEY3)
    __BUTTON_KEY4 = Button(__PIN_KEY4)


    __BUTTON_KEY1.when_pressed = KEY1_PRESSED.notify
    __BUTTON_KEY2.when_pressed = KEY2_PRESSED.notify
    __BUTTON_KEY3.when_pressed = KEY3_PRESSED.notify
    __BUTTON_KEY4.when_pressed = KEY4_PRESSED.notify


except:
    logging.warning("Failed to import gpiozero, Buttons will not work!")
    logging.info("Setting up alternative button emulation, input '1', '2', '3' or '4' into the terminal window")

    __run = True
    def get_input():
        global __run
        while __run:
            x = sys.stdin.read(1)
            if x == "1":
                KEY1_PRESSED.notify()
            elif x == "2":
                KEY2_PRESSED.notify()
            elif x == "3":
                KEY3_PRESSED.notify()
            elif x == "4":
                KEY4_PRESSED.notify()

    t = Thread(target=get_input, daemon=True)
    t.start()

    def stop_thread():
        logging.debug("Stopping input thread")
        global __run
        __run = False

    reactor.addSystemEventTrigger("before", "shutdown", stop_thread)

