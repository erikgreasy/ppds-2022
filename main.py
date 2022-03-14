from random import randint
from time import sleep
from fei.ppds import Mutex, Thread, Semaphore, Event, print


class Lightswitch:
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
    access_data = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()

    for monitor_id in range(8):
        Thread(
            monitor,
            monitor_id,
            valid_data,
            turniket,
            ls_monitor,
            access_data)

    Thread(sensorPT, 0, turniket, ls_sensor, valid_data, access_data)
    Thread(sensorPT, 1, turniket, ls_sensor, valid_data, access_data)
    Thread(sensorH, 2, turniket, ls_sensor, valid_data, access_data)


def monitor(monitor_id, valid_data, turniket, ls_monitor, access_data):
    valid_data.wait()

    while True:
        sleep(randint(50, 60) / 1000)
        turniket.wait()
        num_of_writing_monitors = ls_monitor.lock(access_data)
        turniket.signal()

        sleep(randint(40, 50) / 1000)
        print(f'monit "{monitor_id:02d}": '
              f'num_of_writing_monitors={num_of_writing_monitors:02d}')
        ls_monitor.unlock(access_data)


def sensorPT(sensor_id, turniket, ls_sensor, valid_data, access_data):
    while True:
        turniket.wait()
        turniket.signal()

        num_of_writing_sensors = ls_sensor.lock(access_data)
        writing_process = randint(10, 20) / 1000
        print(f'sensor "{sensor_id:02d}": '
              f'num_of_writing_sensors={num_of_writing_sensors:02d}, '
              f'writing_process={writing_process:5.3f}')
        sleep(writing_process)
        valid_data.signal()
        ls_sensor.unlock(access_data)


def sensorH(sensor_id, turniket, ls_sensor, valid_data, access_data):
    while True:
        turniket.wait()
        turniket.signal()

        num_of_writing_sensors = ls_sensor.lock(access_data)
        writing_process = randint(20, 25) / 1000
        print(f'sensor "{sensor_id:02d}": '
              f'num_of_writing_sensors={num_of_writing_sensors:02d}, '
              f'writing_process={writing_process:5.3f}')
        sleep(writing_process)
        valid_data.signal()
        ls_sensor.unlock(access_data)


if __name__ == '__main__':
    init()
