from Diploma.VkMACHINERY import VkMACHINERY
from Diploma.utils import pattern_access_token
from Diploma import POINT_OF_AGE, POINT_OF_MUSIC, POINT_OF_BOOKS, POINT_OF_FRIEND_UNIT, POINT_OF_GROUP_UNIT, OAUTH_LINK
from Diploma import SERVICE_TOKEN, VERSION_VK_API

from datetime import datetime

import weakref
import re
from typing import Dict, List, AnyStr


class TinderUser:
    _instances_of_tinder_user = set()

    def __init__(self, init_obj=None):
        self._instances_of_tinder_user.add(weakref.ref(self))
        self._SERVICE_TOKEN = SERVICE_TOKEN

        self.first_name = None
        self.last_name = None
        self.tinder_user_id = None

        self.sex = None
        self.age = None
        self.country = None
        self.city = None

        self.groups = []
        self.friends = []
        self.top3_photos = []

        self.movies = ''
        self.music = ''
        self.books = ''

        self.score = 0

        self.default_request_headers = {
            'access_token': self._SERVICE_TOKEN,
            'v': VERSION_VK_API,
        }

        if init_obj is not None:
            self.init_tinder_user_from_obj(init_obj)

    def init_tinder_user_from_obj(self, obj: Dict):
        self.tinder_user_id = obj['id']
        self.default_request_headers['user_id'] = self.tinder_user_id

        self.first_name = obj['first_name']
        self.last_name = obj.get('last_name', 'closed')

        self.country = obj.get('country', 'closed')
        self.sex = obj.get('sex', 'closed')
        self.movies = obj.get('movies', 'closed')
        self.books = obj.get('books', 'closed')
        self.music = obj.get('music', 'closed')

        self.friends = self.get_friend_list(param=self.default_request_headers)
        self.groups = self.get_groups(param=self.default_request_headers)

        try:
            self.age = int(int(datetime.now().year)) - int(obj['bdate'][-4:])
        except (KeyError, ValueError):
            self.age = 'closed'

    def get_friend_list(self, param):
        return VkMACHINERY.send_request(method='friends.get',
                                        params_of_query=param)['response']['items']

    def get_groups(self, param):
        return VkMACHINERY.send_request(method='users.getSubscriptions',
                                        params_of_query=param)['response']['groups']['items']

    def calculate_matching_score(self, target_user):
        groups_score = self._get_points_of_groups(target_user.groups)
        friends_score = self._get_points_of_friends(target_user.friends)
        books_score = self._get_points_of_books(target_user.books)
        music_score = self._get_points_of_music(target_user.music)
        age_score = self._get_points_of_age(target_user.desired_age_from, target_user.desired_age_to)

        self.score = groups_score + friends_score + books_score + music_score + age_score

    def _get_points_of_groups(self, other_group_list: List):
        return POINT_OF_GROUP_UNIT * len((set(self.groups).intersection(set(other_group_list))))

    def _get_points_of_friends(self, other_friend_list: List):
        return POINT_OF_FRIEND_UNIT * len((set(self.friends).intersection(set(other_friend_list))))

    def _get_points_of_music(self, other_music: AnyStr):
        other_music = set(other_music.split())
        other_music2 = set(self.music.split())
        return POINT_OF_MUSIC * len(other_music.intersection(other_music2))

    def _get_points_of_books(self, other_books: AnyStr):
        other_books = set(other_books.split())
        other_books2 = set(self.books.split())
        return POINT_OF_BOOKS * len(other_books.intersection(other_books2))

    def _get_points_of_age(self, age_from, age_to):
        if self.age != 'closed' and age_from <= self.age <= age_to:
            return POINT_OF_AGE
        else:
            return 0

    def _get_photos_of_user(self):
        params = {'owner_id': self.tinder_user_id, 'album_id': 'profile', 'extended': 1}
        params.update(self.default_request_headers)

        photos = VkMACHINERY.send_request(method='photos.get', params_of_query=params)['response']['items']
        photos.sort(key=lambda ph: int(ph['likes']['count']))

        SIZE = 0
        for ph in photos[-3:]:
            self.top3_photos.append(ph['sizes'][SIZE]['url'])

    def _get_user_in_dict(self):
        self._get_photos_of_user()

        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'vk_link': f'https://vk.com/{self.tinder_user_id}',
            'photos': self.top3_photos
        }

    @classmethod
    def get_tinder_users(cls):
        dead = set()
        for ref in cls._instances_of_tinder_user:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances_of_tinder_user -= dead

    def __repr__(self):
        return f'Tinder User: name: {self.first_name}, uid: {self.tinder_user_id}'


class MainUser(TinderUser):
    def __init__(self):
        super().__init__()

        self.user_token = None
        self.user_id = None
        self.screen_name = None
        self.desired_age_from = None
        self.desired_age_to = None

        self.default_params_of_request = {
            'access_token': self.user_token,
            'v': VERSION_VK_API,
            'user_token': None
        }

        self.init_main_user()

    def get_access_token(self):
        print(f'get on this link\nand give please browser string\n{OAUTH_LINK}')

        link_after_oauth = 'https://oauth.vk.com/blank.html#access_token=cc65b07c2bf7da48d2f71f36870d5b0052b95e' \
                           '9d36af95e3172829210cf052cf901f129149eb266df626f&expires_in=86400&user_id=211809712'

        return re.sub(pattern_access_token, r'\3', link_after_oauth)

    def init_main_user(self):
        self.user_token = self.get_access_token()
        self.default_params_of_request['access_token'] = self.user_token

        params_of_request = {'fields': 'sex,bdate,city,country,activities,interests,music,movies,books'}
        params_of_request.update(self.default_params_of_request)

        profile_info = VkMACHINERY.send_request(method='users.get', params_of_query=params_of_request)['response'][0]

        self.first_name = profile_info['first_name']
        self.last_name = profile_info['last_name']
        self.sex = profile_info['sex']
        self.age = int(int(datetime.now().year)) - int(profile_info['bdate'][-4:])
        self.city = profile_info['city']['id']
        self.movies = profile_info['movies']
        self.music = profile_info['music']
        self.books = profile_info['books']

        self.friends = self.get_friend_list(param=self.default_params_of_request)
        self.groups = self.get_groups(param=self.default_params_of_request)

    def users_search(self):
        age_from = 15
        age_to = 25

        self.desired_age_from = age_from
        self.desired_age_to = age_to

        params_of_request = {'count': 30,
                             'fields': f'sex={(self.sex % 2) + 1},city={self.city},age_from={age_from},age_to={age_to}'}
        params_of_request.update(self.default_params_of_request)

        return VkMACHINERY.send_request(method='users.search', params_of_query=params_of_request)[
            'response']['items']

    def __repr__(self):
        return f'MainUser: name {self.first_name}'
