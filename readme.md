# Class 4 - Nuclear power plant synchronization
Fourth class focus on implementation of nuclear power plant, containing of multiple rods sending signals in parallel. Synchronization problem consist of monitoring entities that receive signal and display the incoming data.

## Analysis
The main synchronization problem in this exercise is modification of the readers and writers problem. The rods are trying to write data by sending signal, so they can be specified as writers. The monitors are reading the singals so in this situation, they act as writers.

## Pseudocode
```
class Lightswitch:
    """Implementation of lightswitch synchronization data structure."""

    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()

        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def init():
    """Main program code."""
    access_data = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()

    for monitor_id in <0,8>:
        create_and_run_thread(monitor, monitor_id)

    create_and_run_thread(sensorPT, 0)
    create_and_run_thread(sensorPT, 1)
    create_and_run_thread(sensorH, 2)


def monitor(monitor_id, valid_data, turniket, ls_monitor, access_data):
    """Function acting as monitor reading in power plant"""
    valid_data.wait()

    while True:
        sleep(50 or 60 ms)
        turniket.wait()
        num_of_writing_monitors = ls_monitor.lock(access_data)
        turniket.signal()

        sleep(40 or 50ms)
        print(f'monit "{monitor_id:02d}": '
              f'num_of_writing_monitors={num_of_writing_monitors:02d}')
        ls_monitor.unlock(access_data)


def sensorPT(sensor_id, turniket, ls_sensor, valid_data, access_data):
    """Sensor of type P and T in power plant."""
    while True:
        turniket.wait()
        turniket.signal()

        num_of_writing_sensors = ls_sensor.lock(access_data)
        writing_process = 10 or 20 ms
        print(f'sensor "{sensor_id:02d}": '
              f'num_of_writing_sensors={num_of_writing_sensors:02d}, '
              f'writing_process={writing_process:5.3f}')
        sleep(writing_process)
        valid_data.signal()
        ls_sensor.unlock(access_data)


def sensorH(sensor_id, turniket, ls_sensor, valid_data, access_data):
    """Sensor of type H in power plant."""
    while True:
        turniket.wait()
        turniket.signal()

        num_of_writing_sensors = ls_sensor.lock(access_data)
        writing_process = 20 or 25 ms
        print(f'sensor "{sensor_id:02d}": '
              f'num_of_writing_sensors={num_of_writing_sensors:02d}, '
              f'writing_process={writing_process:5.3f}')
        sleep(writing_process)
        valid_data.signal()
        ls_sensor.unlock(access_data)
```

## Running the program
Run the program with:
```
python main.py
```
