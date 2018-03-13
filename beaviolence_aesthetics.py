def created_time():
    import time
    format = '%Y-%m-%d'
    value = time.localtime(time.time())
    dt = time.strftime(format, value)
    return dt


s = created_time()

print(s, type(s))