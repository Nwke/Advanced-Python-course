import time
import Function.advanced_print


def logger(path_log_file):
    count_call = 0
    start_session_log = True

    def decor(old_function):

        def wrapper(*args, **kwargs):
            nonlocal count_call, start_session_log
            count_call += 1

            ret_value = old_function(*args, **kwargs)
            name = old_function.__name__
            call_time = time.time()
            with open(path_log_file, 'a', encoding='utf8') as log_file:
                if start_session_log:
                    log_file.write('======= Log session is start ======= \n')
                    start_session_log = False
                log_file.write(f'{count_call} {name}, {ret_value}, {call_time}, {args}, {kwargs} \n')

            return ret_value

        return wrapper

    return decor


@logger('logger_do_something.txt')
def advanced_print(*args, **kwargs):
    Function.advanced_print.advanced_print(args, kwargs)


advanced_print(5)
