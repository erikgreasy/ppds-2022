"""
Copyright 2022 Erik Masny.

Implementation of fibonacci sequence with threads and semaphors.
"""

from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Semaphore, print


class Fibonacci:
    """Fibonacci sequence class including the array with sequence"""

    def __init__(self):
        self.list = [0, 1]
        self.M = Mutex()
        self.T = Semaphore(0)

    def add(self, i):
        self.M.lock()
        if len(self.list) == i + 2:
            self.list.append(self.list[-1] + self.list[-2])
            self.T.signal(i)
        self.M.unlock()
        self.T.wait()


def count_element(fb, i):
    """Function calling fibonacci class to count the element of the sequence"""
    sleep(randint(1, 10) / 10)
    print('Count bro ' + str(i))
    fb.add(i)
    print(fb.list)


fb = Fibonacci()

threads = [Thread(count_element, fb, i) for i in range(20)]
[t.join() for t in threads]
