from Diploma.VkMACHINERY import VkMACHINERY
from Diploma.TinderUsers import TinderUser, MainUser

from pprint import pprint
import json


def tact_of_app(main_user):
    list_tinder_users = []

    for tinder_user in TinderUser.get_tinder_users():
        tinder_user.calculate_matching_score(main_user)
        list_tinder_users.append(tinder_user)

    list_tinder_users.sort(key=lambda user: user.score)

    top10 = list_tinder_users[-11:]
    top10.pop(-1)  # mainUser is instance of TinderUser, we have to pop him
    result = []

    for user in top10:
        result.append(user._get_user_in_dict())

    pprint(json.dumps(result))


def run_app():
    main_user = MainUser()

    tinder_users = []

    data_of_users = VkMACHINERY.get_data_tinder_users(main_user)

    for data_user in data_of_users:
        tinder_users.append(TinderUser(init_obj=data_user))

    tact_of_app(main_user)


if __name__ == '__main__':
    run_app()
