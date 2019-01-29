import time


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
def advanced_print(*args, start='', max_line=10, in_file=False, sep=' ', end='\n', **kwargs):
    full_string_prepare = [str(arg) for arg in args]
    full_string = sep.join(full_string_prepare)
    res_str = ''

    if len(full_string) + len(start) + len(args) * len(sep) < max_line:
        res_str = f'{start}'
        for ind, arg in enumerate(args):
            sep = sep if ind != 0 else ''
            res_str += f'{sep}{arg}'

    else:
        for i in range(0, len(full_string), max_line):
            substr = full_string[i: i + max_line]

            sep = sep if i != 0 else ''

            res_str += f'{sep}{substr}\n'

    print(res_str, end=end)

    file_path = ''

    if in_file:
        for k, v in kwargs.items():
            if k == 'file':
                file_path = kwargs[k]

        if file_path == '':
            raise FileNotFoundError

        with open(file_path, 'a') as file:
            res_str += f'{end}'
            file.write(res_str)


advanced_print(5)
