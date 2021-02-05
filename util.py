from threading import Timer


def set_interval(interval, callback) -> Timer:
    def wrapper():
        set_interval(interval, callback)
        callback()

    t = Timer(interval, wrapper)
    t.start()
    return t
