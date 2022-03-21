"""Copyright 2022 Erik Masny.

Dinning savages problem implementation.
"""

from fei.ppds import Semaphore, Mutex, Thread, print, Event
from random import randint
from time import sleep

"""M and N are model params and not synchronization params.
Therefore we dont put them in shared object.

    M - number of portions
    N - number of savages (wihtout cook)
    C - number of cooks
"""
M = 2
N = 3
C = 3


class SimpleBarrier:
    """Implementation of barrier with custom outputs."""

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    """Shared object collecting all synchronization variables."""

    def __init__(self):
        self.mutex = Mutex()
        self.cook_mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


def get_serving_from_pot(savage_id, shared):
    """Remove serving from shared object."""

    print("savage %2d: taking the serving" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("savage %2d: eating" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        """Savage implementation."""

        shared.barrier1.wait(
            "savage %2d: came for dinner, there is %2d of us",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("savage %2d: we are all, lets eat",
                             savage_id,
                             print_last_thread=True)

        shared.mutex.lock()
        print("savage %2d: portions left %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("savage %2d: wake up cook" % savage_id)
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def put_servings_in_pot(cook_id, M, shared):
    """Update shared variable servings.

    M - num of portions cooked
    """

    print(f"cook {cook_id}: putting servings to pot")
    sleep(0.4 + randint(0, 2) / 10)

def cook_serving(cook_id, shared):
    print(f"cook {cook_id}: cooking portion")
    sleep(0.4 + randint(0, 2) / 10)
    shared.servings += 1
    print(f"cook {cook_id}: finished cooking portion")



def cook(cook_id, M, shared):
    """Cook implementation, cooking the servings.

    M - num of portions to cook
    """

    while True:
       
        shared.empty_pot.wait()
        shared.cook_mutex.lock()
        if shared.servings == M:
            print(f'cook {cook_id} putting servings to pot')
            put_servings_in_pot(cook_id, M, shared)
            # shared.cook_mutex.unlock()
            shared.full_pot.signal()
            shared.empty_pot.clear()
            shared.empty_pot.wait()

        cook_serving(cook_id, shared)
        shared.cook_mutex.unlock()



def init_and_run(N, M):
    """Run the module."""
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared))
    for cook_id in range(0, C):
        threads.append(Thread(cook, cook_id, M, shared))
        

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M)
