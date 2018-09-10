"""Output numbers from 0..100 in order.
First thread outputs even numbers.
Second thread outputs odd numbers."""

import threading

MAX = 100
condition = threading.Condition()
result = []


def print_even():
    for i in range(0, MAX + 1, 2):
        with condition:
            print("Thread 1: {}".format(i))
            result.append(i)
            condition.notify()
            if i < MAX:
                condition.wait()


def print_odd():
    for i in range(1, MAX + 1, 2):
        with condition:
            print("Thread 2: {}".format(i))
            result.append(i)
            condition.notify()
            condition.wait()


if __name__ == '__main__':
    thread_even = threading.Thread(target=print_even)
    thread_odd = threading.Thread(target=print_odd)
    thread_even.start()
    thread_odd.start()

    thread_even.join()
    thread_odd.join()
    print("PASS" if result == [i for i in range(0, MAX + 1)] else "FAIL")
