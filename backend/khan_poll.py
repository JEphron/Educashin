import threading


def work():
    threading.Timer(2, work).start()


work()
