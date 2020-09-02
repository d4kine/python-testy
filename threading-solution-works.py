import threading
import time
import logging

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

    threads = list()

    kleinanzeigen_thread = threading.Thread(target=t1.error_test)
    threads.append(kleinanzeigen_thread)
    kleinanzeigen_thread.start()

    immoscout_thread = threading.Thread(target=t2.method)
    threads.append(immoscout_thread)
    immoscout_thread.start()

    kalaydo_thread = threading.Thread(target=t3.sleep_method)
    threads.append(kalaydo_thread)
    kalaydo_thread.start()

    retval_thread = threading.Thread(target=t4.return_a_value)
    threads.append(retval_thread)
    retval_thread.start()

for t in threads:
    t.join()
