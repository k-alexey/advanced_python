"""Output numbers from 0..100 in order.
First thread outputs even numbers.
Second thread outputs odd numbers."""

import threading
import time

MAX = 100
TIMEOUT = 0.1
result = []


def print_even():
    for i in range(0, MAX + 1, 2):
        print("Thread 1: {}".format(i))
        result.append(i)
        time.sleep(TIMEOUT)


def print_odd():
    for i in range(1, MAX + 1, 2):
        print("Thread 2: {}".format(i))
        result.append(i)
        time.sleep(TIMEOUT)


if __name__ == '__main__':
    threading.Timer(TIMEOUT / 2.0, print_even).start()
    threading.Timer(TIMEOUT, print_odd).start()

    while threading.active_count() > 1:
        time.sleep(0.2)
    print("PASS" if result == [i for i in range(0, MAX + 1)] else "FAIL")
