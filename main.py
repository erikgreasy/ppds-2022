"""Copyright 2022 Erik Masny.

H20 synchronization problem.
"""

from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread, print


class Shared:
    """Shared object storing synchronization variables."""

    def __init__(self):
        self.oxygen = 0
        self.hydrogen = 0
        self.mutex = Mutex()
        self.barrier = SimpleBarrier(3)
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)


class SimpleBarrier:
    """Implementation of simple barrier."""

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
            self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()


def bond(shared):
    """Function imitating creation of H20 molecule."""

    print('H2O created')
    sleep(1)


def oxygen(shared):
    """Function imitating creating oxygen."""

    while True:
        shared.mutex.lock()
        print('creating oxygen')
        sleep(randint(0, 10) / 100)
        shared.oxygen += 1

        if shared.hydrogen < 2:
            shared.mutex.unlock()
        else:
            shared.oxygen -= 1
            shared.hydrogen -= 2
            shared.oxyQueue.signal()
            shared.hydroQueue.signal(2)

        print('lets wait for oxy queue')

        shared.oxyQueue.wait()

        bond(shared)

        shared.barrier.wait()
        shared.mutex.unlock()


def hydrogen(shared):
    """Function imitating creating hydrogen."""

    while True:
        shared.mutex.lock()
        print('creating hydrogen')

        sleep(randint(0, 10) / 100)
        shared.hydrogen += 1

        if shared.hydrogen < 2 or shared.oxygen < 1:
            shared.mutex.unlock()
        else:
            shared.oxygen -= 1
            shared.hydrogen -= 2
            shared.oxyQueue.signal()
            shared.hydroQueue.signal(2)

        print('lets wait for hydro queue')
        shared.hydroQueue.wait()
        shared.barrier.wait()


def main():
    """Main function creating threads and objects."""

    shared = Shared()

    threads = []
    threads.append(Thread(oxygen, shared))
    threads.append(Thread(hydrogen, shared))
    threads.append(Thread(hydrogen, shared))

    [t.join() for t in threads]


if __name__ == '__main__':
    main()
