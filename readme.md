# Class 6 - H20 synchronization problem
This class is oriented in solving H20 synchronization problem, where multiple threads are running acting as hydrogen or oxygen molecules. The problem is that we need to combine 2 hydrogens with one oxygen to create H20 molecule as expected.

## Solution
The solution for this problem is to use queues for hydrogen and oxygen for correct ordering and functionality. We implement this with the use of semaphors and global counters for hydrogen and oxygen stored in Shared object.

## Run the program
To run the program, execute following command:
```
python main.py
```
