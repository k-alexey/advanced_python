"""Output numbers from 0..100 in order.
First thread outputs even numbers.
Second thread outputs odd numbers."""

import threading
import time

MAX = 100
TIMEOUT = 0.000001
result = []


def print_even(i):
    print("Thread 1: {}".format(i))
    result.append(i)
    if i < MAX:
        threading.Timer(TIMEOUT, print_odd, [i + 1]).start()


def print_odd(i):
    print("Thread 2: {}".format(i))
    result.append(i)
    threading.Timer(TIMEOUT, print_even, [i + 1]).start()


if __name__ == '__main__':
    threading.Timer(TIMEOUT, print_even, [0]).start()

    while threading.active_count() > 1:
        time.sleep(0.2)
    print("PASS" if result == [i for i in range(0, MAX + 1)] else "FAIL")
