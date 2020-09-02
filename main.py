import threading
import time
import logging
from queue import Queue

class Test(object):

    def method(self):
        logging.debug('Starting')
        print("normal process")
        logging.debug('Exiting')

    def sleep_method(self):
        logging.debug('Starting')
        time.sleep(2)
        logging.debug('Exiting')
        print("sleeping process")

    def error_test(self):
        logging.debug('Starting')
        time.sleep(0.5)
        logging.debug('Exiting')
        raise Exception("Sorry, no numbers below zero")

    def return_a_value(self):
        logging.debug('Starting')
        return 10

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

if __name__ == "__main__":
    
    t1 = Test()
    t2 = Test()
    t3 = Test()
    t4 = Test()

    q = Queue()
    threads = list()

    kleinanzeigen_thread = threading.Thread(target=q.put(t1.error_test), args=(q))
    threads.append(kleinanzeigen_thread)
    kleinanzeigen_thread.start()

    immoscout_thread = threading.Thread(target=q.put(t2.method), args=(q))
    threads.append(immoscout_thread)
    immoscout_thread.start()

    kalaydo_thread = threading.Thread(target=q.put(t3.sleep_method), args=(q))
    threads.append(kalaydo_thread)
    kalaydo_thread.start()

    retval_thread = threading.Thread(target=q.put(t4.return_a_value), args=(q))
    threads.append(retval_thread)
    retval_thread.start()

    for t in threads:
        t.join()

    while not q.empty():
        result = q.get()
        print(result)