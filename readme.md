# Exercise 1
This branch consists of file main.py and few other files named mutex.py with index.

The file **main.py** includes core programm code, that initializes array and two threads writing in that array. The goal of this exercise is to use locks to prevent threads interrupt continuos parallel writing to array, simply said, to make every item in array be written just by one thread.

## mutex1.py
In this file, I put the lock outside the loop in do_count function, which results in locking by first thread, and the second thread is waiting until the whole loop is finished. That way the first thread writes to whole array and second thread doesn't write at all.

Run the programm with:
```
python mutex1.py
````
