import requests
from Diploma import SERVICE_TOKEN, VERSION_VK_API


class VkMACHINERY:
    @staticmethod
    def send_request(method, params_of_query=None):
        return requests.get(f'https://api.vk.com/method/{method}', params=params_of_query).json()

    @staticmethod
    def get_data_tinder_users(main_user):
        opened_tinder_user_ids = []
        searched_users = main_user.users_search()

        for searched_user in searched_users:
            if searched_user['is_closed'] is False:
                opened_tinder_user_ids.append(str(searched_user['id']))

        get_users_param = {
            'access_token': SERVICE_TOKEN,
            'v': VERSION_VK_API,
            'user_ids': ','.join(opened_tinder_user_ids),
            'fields': 'sex,bdate,city,country,activities,interests,music,movies,books'
        }

        data_of_tinder_users = VkMACHINERY.send_request('users.get', params_of_query=get_users_param)['response']

        return data_of_tinder_users
