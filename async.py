"""Copyright 2022 Erik Masny.

Asynchronous version of Chuck Puller - app to pull jokes about Chuck Norris.
"""

import asyncio
import aiohttp
import time
import platform


async def get_jokerino(i):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.chucknorris.io/jokes/random') as res:
            res = await res.json()
            print(f"{i}: {res['value']}")


async def main():

    start = time.time()

    for i in range(20):
        await get_jokerino(i)

    end = time.time()
    print(end - start)

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
