import hashlib


def get_hash(obj):
    return hashlib.md5(obj.encode('utf-8')).hexdigest()


def hash_file(path):
    with open(path, encoding='utf8') as f:
        for line in f:
            yield get_hash(line)


for hashed_line in hash_file('new_countries.txt'):
    print(hashed_line)
