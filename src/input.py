import logging
from threading import Thread


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

    KEY1_PRESSED.subscribe(lambda: logging.debug("KEY1 pressed!"))
    KEY2_PRESSED.subscribe(lambda: logging.debug("KEY2 pressed!"))
    KEY3_PRESSED.subscribe(lambda: logging.debug("KEY3 pressed!"))
    KEY4_PRESSED.subscribe(lambda: logging.debug("KEY4 pressed!"))

except:
    logging.warning("Failed to import gpiozero, Buttons will not work!")
