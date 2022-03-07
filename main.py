"""Copyright 2022 Erik Masny.

Producer consumer problem with experiments with values.
"""

from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread, print
import matplotlib.pyplot as plt


class Shared(object):
    """Object storing shared data."""

    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.counter = 0
        self.free = Semaphore(N)
        self.items = Semaphore(0)


def producer(shared, item_produce_time):
    while True:
        # production
        sleep(item_produce_time / 100)
        # check space in storage
        shared.free.wait()

        if shared.finished:
            break
        # get total access to storage
        shared.mutex.lock()
        # save item to storage
        shared.counter += 1
        # leave the storage
        shared.mutex.unlock()
        # update stock in storage
        shared.items.signal()


def consumer(shared, item_consume_time):
    while True:
        # check stock in storage
        shared.items.wait()

        if shared.finished:
            break
        # get access to storage
        shared.mutex.lock()
        # get item from storage
        shared.counter -= 1
        # leave the storage
        shared.mutex.unlock()
        # process the item
        sleep(item_consume_time / 100)


def plot(results):
    """Print results of experiment in plot."""
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = [a[0] for a in results]
    y = [a[1] for a in results]
    z = [a[2] for a in results]
    ax.set_xlabel('Production time')
    ax.set_ylabel('Num of consumers')
    ax.set_zlabel('Items per second')

    ax.plot_trisurf(x, y, z)
    plt.show()


def main():
    """Experiment function testing different item produce times and consumers.

    Code inspired by Matus Jokay in video
    https://www.youtube.com/watch?v=vI_DA3WiijI
    """
    results = []

    for item_produce_time in range(5):
        for n_consumers in range(1, 5):
            items_per_second_sum = 0
            for iteration in range(10):
                s = Shared(10)
                c = [Thread(consumer, s, 6) for _ in range(n_consumers)]
                p = [Thread(producer, s, item_produce_time) for _ in range(5)]

                sleep(0.05)
                s.finished = True

                s.items.signal(100)
                s.free.signal(100)
                [t.join() for t in c + p]

                produced_items = s.counter
                items_per_second = produced_items / 0.05
                items_per_second_sum += items_per_second
            avg_items_per_second = items_per_second_sum / 10

            results.append(
                (item_produce_time, n_consumers, avg_items_per_second)
            )

    print(results)
    plot(results)


if __name__ == '__main__':
    main()
