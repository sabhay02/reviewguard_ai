# utils/timer.py

import time

execution_times = {}


def measure(name):
    def decorator(func):
        def wrapper(state):
            start = time.perf_counter()

            result = func(state)

            execution_times[name] = time.perf_counter() - start

            return result

        return wrapper
    return decorator