import threading
import logging
import time
from multiprocessing import Pool




def f(x):
    return x*x

if __name__ == '__main__':
    pool = Pool(processes=4)              # start 4 worker processes
    result = pool.apply_async(f, [10])     # evaluate "f(10)" asynchronously
    print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"



#worker.setDaemon(True)    #setting threads as "daemon" allows main program to 
                              #exit eventually even if these dont finish 
                              #correctly.
#worker.start()

# def test():
#     t1 = threading.Thread(target=my_function(1))
#     t1.setDaemon(True)

#     t2 = threading.Thread(target=my_function(2))
#     t2.setDaemon(True)

#     t3 = threading.Thread(target=my_function(3))
#     t3.setDaemon(True)

#     t1.start()
#     t2.start()
#     t3.start()



# p1 = multiprocessing.Process(target=my_function, args=(1))
# p1.start()
# p1.join()


# p2 = multiprocessing.Process(target=my_function, args=(1))
# p2.start()
# p2.join()
