"""
Copyright 2022 Erik Masny.

Implementation of simple barrier with use of semaphors.
"""

from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print


class SimpleBarrier:
    """Implementation of simple barrier """

    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()


def barrier_example(barrier, thread_id):
    """Example function used in threads to act as barrier using simple barrier class"""
    sleep(randint(1, 10) / 10)
    print("thread %d before barrier" % thread_id)
    barrier.wait()
    print("thread %d after barrier" % thread_id)


sb = SimpleBarrier(5)

threads = [Thread(barrier_example, sb, i) for i in range(5)]
[t.join() for t in threads]
