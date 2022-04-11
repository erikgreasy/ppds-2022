# Class 7 - coprograms
This lesson is the first one in the section of multiple classes on topic of asynchronous programming. Goal is to implement an that has multiple coprograms with the use of extended generators, whose execution is handled by simple scheduler.

## Implemented example
The example in the main.py contains code for multiple greps running "at the same time" - with the help of the dispatcher, file get opened only one time, and greps goes through lines, giving each other space to run for the line. The code itself is taken from the class, all credits for the program goes to our teacher Mgr Ing Mr Jokay PhD.

## Run the program
Run the program with 
```
python main.py
```