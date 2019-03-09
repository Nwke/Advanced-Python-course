from Diploma.VkMACHINERY import VkMACHINERY
from Diploma.utils import pattern_access_token
from Diploma import POINT_OF_AGE, POINT_OF_MUSIC, POINT_OF_BOOKS, POINT_OF_FRIEND_UNIT, POINT_OF_GROUP_UNIT, OAUTH_LINK
from Diploma import SERVICE_TOKEN, VERSION_VK_API
from Diploma import DB_USER, DB_NAME

from datetime import datetime
from typing import Dict, List, AnyStr

import re
import psycopg2 as pg


class TinderUser:
    # todo: there is a memory leak
    _instances_of_tinder_user = []

    def __init__(self, init_obj=None):
        self._instances_of_tinder_user.append(self)
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

        self.request_header_for_tinder_user = {
            'access_token': self._SERVICE_TOKEN,
            'v': VERSION_VK_API,
        }

        if init_obj is not None:
            self.init_tinder_user_from_obj(init_obj)

    def init_tinder_user_from_obj(self, obj: Dict):
        self.tinder_user_id = obj['id']
        self.request_header_for_tinder_user['user_id'] = self.tinder_user_id

        self.first_name = obj['first_name']
        self.last_name = obj.get('last_name', 'closed')

        self.country = obj.get('country', 'closed')
        self.sex = obj.get('sex', 'closed')
        self.movies = obj.get('movies', 'closed')
        self.books = obj.get('books', 'closed')
        self.music = obj.get('music', 'closed')

        self.friends = self.get_friend_list(param=self.request_header_for_tinder_user)
        self.groups = self.get_groups(param=self.request_header_for_tinder_user)

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
        params.update(self.request_header_for_tinder_user)

        print(VkMACHINERY.send_request(method='photos.get', params_of_query=params))
        photos = VkMACHINERY.send_request(method='photos.get', params_of_query=params)['response']['items']
        photos.sort(key=lambda photo: int(photo['likes']['count']))

        size = 0
        for ph in photos[-3:]:
            self.top3_photos.append(ph['sizes'][size]['url'])

    def get_user_in_dict(self):
        self._get_photos_of_user()

        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'vk_link': f'https://vk.com/id{self.tinder_user_id}',
            'photos': self.top3_photos
        }

    @classmethod
    def get_tinder_users_for_one_round(cls, count):
        return cls._instances_of_tinder_user[-count:]

    def __repr__(self):
        return f'Tinder User: name: {self.first_name}, uid: {self.tinder_user_id}'


class MainUser(TinderUser):

    def __init__(self, count_for_search=15):
        super().__init__()

        self.user_token = None
        self.screen_name = None
        self.desired_age_from = None
        self.desired_age_to = None
        self.count_for_search = count_for_search
        self.offset_for_search = None

        self.request_header_for_main_user = {
            'access_token': self.user_token,
            'v': VERSION_VK_API,
            'user_token': None
        }

        self._init_main_user()

    def _init_main_user(self):
        self._set_token()
        profile_info = self._get_profile_info()

        self._init_default_params(profile_info)
        self._set_additional_params()

    def _get_access_token(self):
        # todo: there is a mock
        print(f'get on this link\nand give please browser string\n{OAUTH_LINK}')

        link_after_oauth = 'https://oauth.vk.com/blank.html#access_token=8bd71d2cd09e82352b9c1d0e43d8288c103c33b9' \
                           '4d1a5a5e32cd693a273a7b08f4b2480dd66127cff93a1&expires_in=86400&user_id=211809712'

        return re.sub(pattern_access_token, r'\3', link_after_oauth)

    def _set_token(self):
        self.user_token = self._get_access_token()
        self.request_header_for_main_user['access_token'] = self.user_token

    def _set_additional_params(self):
        print('There are search settings save only for session')
        self.desired_age_from = int(input('Give number for desired min of search age: '))
        self.desired_age_to = int(input('Give number for desired max of search age: '))

        with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT current_offset FROM _tinder_service_information WHERE id=(%s)""", ('1',))
                self.offset_for_search = int(cur.fetchone()[0])
                print(self.offset_for_search, '<- SET INITIAL OFFSET SEARCH')

    def _init_default_params(self, profile_info):
        self.tinder_user_id = profile_info['id']
        self.first_name = profile_info['first_name']
        self.last_name = profile_info['last_name']
        self.sex = profile_info['sex']
        self.age = int(int(datetime.now().year)) - int(profile_info['bdate'][-4:])
        self.city = profile_info['city']['id']
        self.movies = profile_info['movies']
        self.music = profile_info['music']
        self.books = profile_info['books']

        self.friends = self.get_friend_list(param=self.request_header_for_main_user)
        self.groups = self.get_groups(param=self.request_header_for_main_user)

    def _get_profile_info(self):
        params_of_request = {'fields': 'sex,bdate,city,country,activities,interests,music,movies,books'}
        params_of_request.update(self.request_header_for_main_user)

        items_of_request = 0
        return VkMACHINERY.send_request(method='users.get', params_of_query=params_of_request)['response'][
            items_of_request]

    def update_search_offset(self):
        with pg.connect(dbname=DB_NAME, user=DB_USER) as conn:
            with conn.cursor() as cur:
                self.offset_for_search += self.count_for_search
                cur.execute("""UPDATE _tinder_service_information SET current_offset=(%s) WHERE id=(%s)""",
                            (self.offset_for_search, '1'))  # this table will have only 1 row so id equal "1"
        print('I DEAD')

    def get_search_config_obj(self):
        return {'count_for_search': self.count_for_search,
                'sex': self.sex,
                'city': self.city,
                'desired_age_from': self.desired_age_from,
                'desired_age_to': self.desired_age_to,
                'offset_for_search': self.offset_for_search}

    def _get_headers(self):
        return self.request_header_for_main_user

    def __repr__(self):
        return f'MainUser: name {self.first_name}'
