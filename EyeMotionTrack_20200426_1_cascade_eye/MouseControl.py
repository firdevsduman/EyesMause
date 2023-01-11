import logging
import threading
import time
import pyautogui 

pyautogui.FAILSAFE=False

def thread_function(name):
    logging.info("Thread %s: starting", name)
    pyautogui.moveTo(0,0, duration = 3)
    logging.info("Thread %s: finishing", name)
    #time.sleep(2)

def thread_function2(name):
    logging.info("Thread %s: starting", name)
    pyautogui.moveTo(1280,1280, duration = 3)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    #x.join()
    logging.info("Main    : all done")
    x2 = threading.Thread(target=thread_function2, args=(2,))
    x2.start()