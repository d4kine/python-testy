import multiprocessing
import traceback
from abc import ABC, abstractmethod

from time import sleep


class Process(multiprocessing.Process):
    """
    Class which returns child Exceptions to Parent.
    https://stackoverflow.com/a/33599967/4992248
    """

    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._parent_conn, self._child_conn = multiprocessing.Pipe()
        self._exception = None

    def run(self):
        try:
            multiprocessing.Process.run(self)
            self._child_conn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._child_conn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._parent_conn.poll():
            self._exception = self._parent_conn.recv()
        return self._exception


class BaseTask(ABC):
    @abstractmethod
    def run(self):
        pass

    def task_run(self, queue):
        queue.put(self.run())


class TaskNormal(BaseTask):
    def run(self):
        print("normal process")
        return 123

class TaskSleep(BaseTask):
    def run(self):
        print("sleeping process")
        sleep(2)
        return None


class TaskError(BaseTask):
    def run(self):
        raise Exception("Sorry, no numbers below zero")


class TaskRetrunVal(BaseTask):
    def run(self):
        return 10


def processes_alive(processes: list):
    for process in processes:
        if not process.is_alive():
            return False

    return True


class TestResult:
    def __init__(self, success: bool, payload: str):
        self.success = success
        self.payload = payload

    def __str__(self):
        return f"TestResult(success={self.success}, payload={self.payload})"

    def __repr__(self):
        return str(self)

def main():

    test_tasks = [TaskRetrunVal(), TaskError(), TaskNormal(), TaskSleep()]
    test_queues = []
    test_processes = []
    test_results = {}


    # Example of multiprocessing which is used:
    # https://eli.thegreenplace.net/2012/01/16/python-parallelizing-cpu-bound-tasks-with-multiprocessing/

    for i, task in enumerate(test_tasks):
        test_queues.append(multiprocessing.Queue())
        test_processes.append(Process(target=task.task_run, kwargs=dict(queue=test_queues[i])))


    for process in test_processes:
        process.start()


    while processes_alive(test_processes):
        sleep(2)
        print(processes_alive(test_processes))

        for i, process in enumerate(test_processes):
            if process.exception:
                error, task_1_traceback = process.exception
                test_results[i] = TestResult(False, error)
                process.terminate()


    for i, process in enumerate(test_processes):
        if i not in test_results.keys(): # we got no exception so there should be a useful result
            test_results[i] = TestResult(True, test_queues[i].get())


    print(test_results)


if __name__ == "__main__":
    main()
