import time
from threading import Timer
from test import getData
def getD():
    ret = getData('BwjZZ2M9QvN7AyN3','Fbn8AHy4XBAAaDbp')#.strip(']').strip('[')
    if len(ret)!=0:
        print ret
        t = Timer(1, getD)
        t.start()
    else:
        return True
getD()