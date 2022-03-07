"""
Copyright 2022 Erik Masny.

Producer consumer problem with experiments with values.
"""

from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread, print


class Shared(object):
    """Object storing shared data"""

    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)


def producer(shared):
    while True:
        # production
        sleep(randint(1, 10) / 10)
        print('P')
        # check space in storage
        shared.free.wait()

        if shared.finished:
            break
        # get total access to storage
        shared.mutex.lock()
        # save item to storage
        sleep(randint(1, 10) / 100)
        # leave the storage
        shared.mutex.unlock()
        # update stock in storage
        shared.items.signal()


def consumer(shared):
    while True:
        # check stock in storage
        shared.items.wait()

        if shared.finished:
            break
        # get access to storage
        shared.mutex.lock()
        # get item from storage
        sleep(randint(1, 10) / 100)
        # leave the storage
        shared.mutex.unlock()
        # process the item
        print('C')
        sleep(randint(1, 10) / 10)


def main():
    s = Shared(10)
    c = [Thread(consumer, s) for _ in range(2)]
    p = [Thread(producer, s) for _ in range(5)]

    sleep(5)
    s.finished = True

    print('main thread: wait to finish')
    s.items.signal(100)
    s.free.signal(100)
    [t.join() for t in c + p]
    print('main thread: end')


if __name__ == '__main__':
    main()
