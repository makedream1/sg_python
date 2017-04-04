import time
import random
from threading import Lock, Thread, current_thread


def worker(file: object, *args):
    """
        worker function writes two strings with random pause to 
    shared file using synchronization primitive
        :param file: file-object
        :return: 
    """
    with Lock():
        file.write(current_thread().name + ': ' + 'started.\n')
        time.sleep(random.random() * 5)
        file.write(current_thread().name + ': ' + 'done.\n')


if __name__ == '__main__':
    file = open('test.txt', 'a')
    for _ in range(10):
        Thread(target=worker, args=(file,)).start()

