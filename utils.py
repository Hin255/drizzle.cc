import os.path
import time
import json


def log(*args, **kwargs):
    format = '%H:%M:%S, %Y-%m-%d'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(type(dt))
    with open('log.txt', 'a', encoding='utf-8 ') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)

