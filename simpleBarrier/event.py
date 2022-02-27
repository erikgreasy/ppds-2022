"""
Copyright 2022 Erik Masny.

Implementation of simple barrier with use of events.
"""

from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Event, print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Event()

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()


def barrier_example(barrier, thread_id):
    """Predpokladajme, ze nas program vytvara a spusta 5 vlakien,
    ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
    zdielany objekt jednoduchej bariery
    """
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


sb = SimpleBarrier(5)

threads = [Thread(barrier_example, sb, i) for i in range(5)]
[t.join() for t in threads]
