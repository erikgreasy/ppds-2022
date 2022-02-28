# Class 2
Second exercise is focused on barrier and tourniquets. This exercise consist of three parts, files for every part are in it's own folder:
1. Simple barrier
2. Reusable barrier
3. Fibonacci

## Simple barrier
This part is focused on implementing barrier in two ways, one with use of semaphors and other with use of events. Both files are pretty simmilar, basically the only difference is in the used class which takes care of everything else under the hood.

Two implementations are stored in two files, named by the implementation used. 

To run the programm, enter:
```
python ./simpleBarrier/semaphor.py
```

or 
```
python ./simpleBarrier/event.py
```


## Fibonacci sequence
In this part the goal is to implement fibonacci sequence with multiple threads writing to one array, each thread writing the i+2nth item of array.

In the fibonacci/semaphor.py is the draft of the implementation, that is currenntly work in progress.
