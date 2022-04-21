"""Copyright 2022 Erik Masny.

Chuck Puller - synchronous app to pull jokes about Chuck Norris.
"""

import json
import requests
import time


def get_jokerino(i):
    res = requests.get('https://api.chucknorris.io/jokes/random').json()
    print(f"{i}: {res['value']}")


def main():

    start = time.time()

    for i in range(20):
        get_jokerino(i)

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()
