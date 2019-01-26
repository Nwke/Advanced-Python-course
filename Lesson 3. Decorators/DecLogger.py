import time


def logger(old_function):
    def wrapper(*args, **kwargs):
        ret_value = old_function(*args, **kwargs)
        name = old_function.__name__
        call_time = time.time()

        with open('logger.txt', 'a', encoding='utf8') as log_file:
            log_file.write(f'{name}, {ret_value}, {call_time}, {args}, {kwargs}')

        return ret_value

    return wrapper


@logger
def do_something(*args, **kwargs):
    print(args, kwargs)


do_something(1, 2)