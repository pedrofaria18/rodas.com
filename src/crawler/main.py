import time
import logging
from multiprocessing import Process, Lock, Value
from multiprocessing import log_to_stderr, get_logger


def add_500_lock(total, lock):
    for i in range(500):
        time.sleep(0.01)
        lock.acquire()
        total.value += 5
        lock.release()


def sub_500_lock(total, lock):
    for i in range(500):
        time.sleep(0.01)
        lock.acquire()
        total.value -= 5
        lock.release()


def main():
    total = Value('i', 0)
    lock = Lock()

    log_to_stderr()
    logger = get_logger()
    logger.setLevel(logging.INFO)

    add_proc = Process(target=add_500_lock, args=(total, lock))
    sub_proc = Process(target=sub_500_lock, args=(total, lock))

    add_proc.start()
    sub_proc.start()

    add_proc.join()
    sub_proc.join()
    print(total.value)


if __name__ == '__main__':
    main()
