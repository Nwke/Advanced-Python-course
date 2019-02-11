import re

pattern_phone = re.compile(r'(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s* |\-*)(\d{3})(\-*)(\d{2})(\-*)(\d{2})', re.MULTILINE)
pattern_names = re.compile(r'^(\w+)(\s{1}|\,{1})(\w+)(\s{1}|\,{1})(\w*)', flags=re.MULTILINE)
patten_additional_phone = re.compile(r'(\(*)(доб\.)(\s*)(\d{4})(\)*)')

path_from_csv = 'phonebook_raw.csv'
path_to_result = 'new_data.csv'

data_from_csv = ''
with open(path_from_csv, encoding='utf8') as f:
    f.readline()
    for row in f:
        data_from_csv += row

res = pattern_phone.findall(data_from_csv)

processed_step1 = re.sub(pattern_phone, r'+7(\4)\7-\9-\11', data_from_csv)
processed_step2 = re.sub(pattern_names, r'\1,\3,\5', processed_step1)
processed_step2 = re.sub(patten_additional_phone, r'\2\4', processed_step2)


def processed(data):
    about_persons = {}
    collisions_person = {}

    for row_person in data.split('\n'):
        all_info_about_person = row_person.split(',')
        last_name, first_name, surname, = row_person.split(',')[:3]
        person_key = last_name + first_name

        if person_key not in about_persons:
            about_persons[person_key] = all_info_about_person
        else:
            collisions_person[person_key] = all_info_about_person

    for key_coll, val_coll in collisions_person.items():
        for unit_info in val_coll:
            if unit_info not in about_persons[key_coll]:
                about_persons[key_coll].append(unit_info)

    return about_persons


processed_data = processed(processed_step2)

with open(path_to_result, 'w', encoding='utf8') as new:
    for key, value in processed_data.items():
        row = ','.join(value)
        row += '\n'
        new.write(row)
