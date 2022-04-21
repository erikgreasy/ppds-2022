# Class 8 - native coroutines with Chuck Norris, aka introducing the Chuck Puller
![](https://images-global.nhst.tech/image/Y0d1UGZGVitSR3dsalB1OHVYQXo3am0yMjVJZXZreXVwWnk0M2YwU1E2cz0=/nhst/binary/8e8a8dbac13b433f7eb809f5dac15c12)

This class's focus is on a concept of native courutines, using python asyncio lib. Goal is to create an example application, first the typical sync way and than transform it into asynchronous application.

## Example application
As an example application, I created the Chuck Puller. Chuck Puller is a simple application, that is using 3rd party REST api to pull in batch of jokes about Chuck Norris. Rumours say that Chuck is sending the jokes by himself, this needs more investigation though. Anyway the app pulls in 20 jokes about Chuck Norris.

The synchronous application is in sync.py and the asynchronous application is in async.py file. After execution, the jokes are printed to STDOUT and the final time elapsed during pulling the jokes is also printed.

## Dependencies
The app is using python libraries, mainly the requests, and aiohttp. You may need to install these first with:
```
pip install requests
```
```
pip install aiohttp
```

## Run the Chuck Puller
To run the synchronous version, execute:
```
python sync.py
```

To run the async version, execute:
```
python async.py
```
