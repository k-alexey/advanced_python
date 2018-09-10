"""Output numbers from 0..100 in order.
First thread outputs even numbers.
Second thread outputs odd numbers."""

import threading

MAX = 100
semaphore_odd = threading.Semaphore(0)
semaphore_even = threading.Semaphore(1)
result = []


def print_even():
    for i in range(0, MAX + 1, 2):
        semaphore_even.acquire()
        print("Thread 1: {}".format(i))
        result.append(i)
        semaphore_odd.release()


def print_odd():
    for i in range(1, MAX + 1, 2):
        semaphore_odd.acquire()
        print("Thread 2: {}".format(i))
        result.append(i)
        semaphore_even.release()


if __name__ == '__main__':
    thread_even = threading.Thread(target=print_even)
    thread_odd = threading.Thread(target=print_odd)
    thread_even.start()
    thread_odd.start()

    thread_even.join()
    thread_odd.join()
    print("PASS" if result == [i for i in range(0, MAX + 1)] else "FAIL")
