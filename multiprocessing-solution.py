import multiprocessing
import time 

class Test(object) :

    def __init__(self):
       self.manager = multiprocessing.Manager()
       self.some_list = self.manager.list()  # Shared Proxy to a list

    def method(self):
        print("normal process")
        self.some_list.append(123) # This change won't be lost

    def sleep_method(self):
        print("sleeping process")
        time.sleep(1)

    def error_test(self):
        raise Exception("Sorry, no numbers below zero")

    def return_a_value(self):
        return 10



if __name__ == "__main__":
    t1 = Test()
    t2 = Test()
    t3 = Test()

    pr1 = multiprocessing.Process(target=t1.sleep_method)
    pr2 = multiprocessing.Process(target=t2.return_a_value)
    pr3 = multiprocessing.Process(target=t3.error_test)

    pr1.start()
    pr2.start()
    pr3.start()

    pr1.join()
    pr2.join()
    pr3.join()

    print(t1.some_list)
    print(t2.some_list)
    print(t2.some_list)