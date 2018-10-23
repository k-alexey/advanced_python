"""Output numbers from 0..100 in order.
First thread outputs even numbers.
Second thread outputs odd numbers."""
from multiprocessing import Pipe
from multiprocessing import Process
MAX = 100
result = []


def print_even(pipe, pipe_result):
    for i in range(0, MAX + 1, 2):
        result = pipe.recv()
        print("Thread 1: {}".format(i))
        result.append(i)
        pipe.send(result)
    pipe_result.send(result)


def print_odd(pipe):
    for i in range(1, MAX + 1, 2):
        result = pipe.recv()
        print("Thread 2: {}".format(i))
        result.append(i)
        pipe.send(result)


if __name__ == '__main__':
    (p_odd, p_even) = Pipe()
    (p_parent, p_child) = Pipe()
    process_even = Process(target=print_even, args=(p_even, p_child))
    process_odd = Process(target=print_odd, args=(p_odd,))
    process_even.start()
    process_odd.start()
    p_odd.send(result)
    result = p_parent.recv()

    print("PASS" if result == [i for i in range(0, MAX + 1)] else "FAIL")
