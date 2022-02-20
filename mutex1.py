from collections import Counter
from dataclasses import asdict
from fei.ppds import Thread, Mutex


class Shared():
    """Wrapper for array with related information about size and current index"""

    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * (size + 10)


def do_count(shared):
    """Execute writing to array with incrementing element and index"""
    mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()


mutex = Mutex()
shared = Shared(1_000_000)

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())
