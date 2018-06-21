import threading
from selenium import webdriver
import time


class MyThread(threading.Thread):

    """Docstring for MyThread. """

    def __init__(self, func, args=()):
        """TODO: to be defined1. """
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        time.sleep(0.1)
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


def main():
    q = webdriver.Chrome()
    print(q)


if __name__ == "__main__":
    s = time.time()
    # driver = []
    for i in range(5):
        task = MyThread(main)
        task.start()
        print(task.get_result())
    e = time.time()
    print(e - s)
