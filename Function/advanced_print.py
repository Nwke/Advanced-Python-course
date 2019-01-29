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


if __name__ == '__main__':
    advanced_print('vanya', 'vasya', 'milenasssssssssv', in_file=True, file='text.txt', sep='*', start='*', end='*')
    advanced_print('hello world')
    advanced_print('We will happy')
