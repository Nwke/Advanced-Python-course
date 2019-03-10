from Tinder import VkMACHINERY
from Tinder.TinderUsers import TinderUser, MainUser
from Tinder.config_app import DB_USER, DB_NAME
from Tinder.config_app import STANDARD_SEARCH_OFFSET
from Tinder.config_app import PATH_TO_OUTPUT_RESULT

from pprint import pprint
from typing import Dict, List

import psycopg2 as pg
import json

def create_db() -> None:
    """
    Create standard databases for the Tinder App
    """

    with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS tinder_result (
                        id serial PRIMARY KEY,
                        first_name varchar(50) NOT NULL,
                        last_name varchar(50) NOT NULL,
                        vk_link varchar(100) UNIQUE NOT NULL);""")

            cur.execute("""CREATE TABLE IF NOT EXISTS tinder_black_list (
            id serial PRIMARY KEY,
            first_name varchar(50),
            last_name varchar(50),
            vk_link varchar(100) UNIQUE NOT NULL);""")

            cur.execute("""CREATE TABLE IF NOT EXISTS tinder_favorite_list (
                        id serial PRIMARY KEY,
                        second_id INTEGER NOT NULL REFERENCES tinder_result(id));""")

            cur.execute("""CREATE TABLE IF NOT EXISTS _tinder_service_information(
                        id INTEGER PRIMARY KEY,
                        current_offset INTEGER);""")


def init_db() -> None:
    """
    Initialize standard databases for the Tinder App
    """

    with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO _tinder_service_information (id, current_offset) VALUES (%s, %s)
                    ON CONFLICT  (id) DO NOTHING """,
                ('1', STANDARD_SEARCH_OFFSET))  # we will have only 1 row in this table


def insert_result_to_db(liked_tinder_users: List[Dict]) -> None:
    """
    Insert result the result of the Tinder App

    :param liked_tinder_users: List of dict of tinder user data
    """

    with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
        with conn.cursor() as cur:
            for user in liked_tinder_users:
                cur.execute("""INSERT INTO tinder_result (first_name, last_name, vk_link) 
                                VALUES (%s, %s, %s) ON CONFLICT (vk_link) DO NOTHING""",
                            (user['first_name'], user['last_name'], user['vk_link']))


def _add_to_black_list(person: Dict) -> None:
    """
    Add person to blacklist in database

    :param person: Dict of user data
    :return:
    """

    with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO tinder_black_list (first_name, last_name, vk_link) VALUES (%s, %s, %s)
                        ON CONFLICT (vk_link) DO NOTHING""",
                        (person['first_name'], person['last_name'], person['vk_link'],))

    print(f'person {person["first_name"]} added to black list')


def _add_to_favorite_list(person: Dict) -> None:
    """
    Add person to favorite list in database

    :param person: Dict of user data
    """

    with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT id FROM tinder_result WHERE vk_link=%s""", (person['vk_link'],))
            id_user_from_table_tinder_result = cur.fetchone()[0]

            cur.execute("""INSERT INTO tinder_favorite_list (second_id) VALUES (%s)""",
                        (id_user_from_table_tinder_result,))

            print(f'person {person["first_name"]} added to favorite list')


def tact_of_app(main_user) -> List[Dict]:
    """
    Do one round of the Tinder app.

    :param main_user: Instance of class MainUser(TinderUser)
    """

    list_tinder_users = []

    for tinder_user in TinderUser.get_tinder_users_for_one_round(main_user.count_for_search):
        tinder_user.calculate_matching_score(main_user)
        list_tinder_users.append(tinder_user)

    list_tinder_users.sort(key=lambda usr: usr.score)

    top10_tinder_users = list_tinder_users[-11:]
    
    # that problem is on the vk side
    # top10.pop(-1)  # we found our self when use vk method users.search

    result_of_matching = []
    for tinder_user in top10_tinder_users:
        result_of_matching.append(tinder_user.get_user_in_dict())

    insert_result_to_db(result_of_matching)
    return result_of_matching


def output_tinder_users(data_of_top10_matching: List[Dict]) -> None:
    """
    Output data of matched Tinder Users to stdout (Name, Photos, ...)

    :param data_of_top10_matching: List of data of Tinder Users
    """

    for ind, data_of_user in enumerate(data_of_top10_matching):
        photos = ''

        for i, ph_link in enumerate(data_of_user['photos']):
            photos = photos + 'photos: {},'.format(ph_link)

        print(f'{ind + 1}.{data_of_user["first_name"]} {data_of_user["last_name"]}, '
              f'vk:{data_of_user["vk_link"]}, {photos}')


def interface_for_black_list(data_of_persons: List[Dict]) -> None:
    """
    Add chosen body to blacklist

    :param data_of_persons: List of data of Tinder Users
    """

    explain_line = 'Get number of person why you want to add to black list'
    chosen_id = _interface_to_add_list(data_of_persons, explain_line)

    _add_to_black_list(data_of_persons[chosen_id])


def interface_for_favorite_list(data_of_persons: List[Dict]) -> None:
    """
    Add person to favorite list in database

    :param data_of_persons: a list of data of Tinder Users from which we will choose who to add to the favorite list
    """

    explain_line = 'Get number of person why you want to add to favorite list'
    chosen_id = _interface_to_add_list(data_of_persons, explain_line)

    _add_to_favorite_list(data_of_persons[chosen_id])


def _interface_to_add_list(data_of_persons: List[Dict], explanatory_line: str) -> int:
    """
    Help function for function with "interface_for_*_list"

    :param data_of_persons: List of data of Tinder Users from which we will chose one
    :param explanatory_line: A string that explains what we will do with the selected person.
    """

    enumerated_person = list(enumerate(data_of_persons))
    while True:
        chosen_id = input(f'{explanatory_line} '
                          f'from {enumerated_person[0][0] + 1} to {enumerated_person[-1][0] + 1}, please: ')
        try:
            chosen_id = int(chosen_id) - 1
            if chosen_id > enumerated_person[-1][0] or chosen_id < enumerated_person[0][0]:
                raise ValueError
            break
        except ValueError:
            print('You did wrong, repeat please')

    return chosen_id


def output_result_to_json(data_of_top10_matching: List[Dict]) -> None:
    """
    Save result of last search to output.json in current working directory

    :param data_of_top10_matching: List of data of Tinder users
    """

    with open(PATH_TO_OUTPUT_RESULT, encoding='utf8', mode='w') as json_output:
        json.dump(data_of_top10_matching, json_output, indent=2)


def run_app():
    main_user = MainUser()
    main_user_config = main_user.get_search_config_obj()
    main_user_request_headers = main_user._get_headers()

    turn_on_the_app = True
    while True and turn_on_the_app:
        main_user_config['offset_for_search'] += main_user.count_for_search
        searched_tinder_users = VkMACHINERY.users_search(main_user_config, main_user_request_headers)
        processed_data_of_tinder_users = VkMACHINERY.get_processed_data_of_tinder_users(searched_tinder_users)

        for data_of_tinder_user in processed_data_of_tinder_users:
            TinderUser(init_obj=data_of_tinder_user)

        main_user.update_search_offset()
        data_of_top10_matching = tact_of_app(main_user)
        output_tinder_users(data_of_top10_matching)

        while True:
            try:
                command = int(input('What are you want to do?\n'
                                    '1.Continue search\n'
                                    '2.Add to favorite list somebody\n'
                                    '3.Add to black list somebody\n'
                                    '4.Print output(10 JSON objects)\n'
                                    '5.Output again\n'
                                    '6.Quit from the app and output result the app to json file \n'
                                    'Your chose: '))

                if command == 1:
                    break
                elif command == 2:
                    interface_for_favorite_list(data_of_top10_matching)
                elif command == 3:
                    interface_for_black_list(data_of_top10_matching)
                elif command == 4:
                    pprint(json.dumps(data_of_top10_matching))
                elif command == 5:
                    output_tinder_users(data_of_top10_matching)
                elif command == 6:
                    turn_on_the_app = False
                    output_result_to_json(data_of_top10_matching)
                    break
                else:
                    raise ValueError('Invalid input')
            except ValueError:
                print('Invalid input, repeat your try')


if __name__ == '__main__':
    create_db()
    init_db()
    run_app()
