from Diploma import SERVICE_TOKEN, VERSION_VK_API
import requests
from typing import Dict, List, Any, Collection, TypeVar

StrOrInt = TypeVar('StrOrInt', str, int)


class VkMACHINERY:
    @staticmethod
    def send_request(method: str, params_of_query: Dict[str, str] = None):
        """
        Send request to the VK API and return a result

        :param str method: Any method from VK API
        :param dict params_of_query: additional params for request
        :return: result of requests.get(...).json()
        """
        return requests.get(f'https://api.vk.com/method/{method}', params=params_of_query).json()

    @staticmethod
    def users_search(config: Dict[str, StrOrInt], headers: Dict) -> List:
        """
        Send request of user.search to VK API and return its result

        :param config: config which use for search similar people
        :param headers: header for send request to vk API (like token and so on)
        :return: List of dict of data similar people
        """
        params_of_request = {'count': config['count_for_search'],
                             'fields': f'sex={(config["sex"] % 2) + 1},city={config["city"]},'
                             f'age_from={config["desired_age_from"]},age_to={config["desired_age_to"]}',
                             'offset': config['offset_for_search']}

        params_of_request.update(headers)

        x = VkMACHINERY.send_request(method='users.search', params_of_query=params_of_request)[
            'response']['items']
        print('HERE3', type(x), x)
        return VkMACHINERY.send_request(method='users.search', params_of_query=params_of_request)[
            'response']['items']

    @staticmethod
    def get_processed_data_of_tinder_users(searched_users):
        """
        Get List of Tinder users and return it processed

        :param List searched_users: List of dict of data
        :return: List of dict of extended data for future initialization
         Tinder Users. Closed profiles will be dropped.
        """
        opened_tinder_user_ids = []

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
