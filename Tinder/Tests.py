from Tinder import VkMACHINERY
from Tinder.TinderUsers import TinderUser, MainUser

import unittest

config = {'count_for_search': 0,
          'sex': 0,
          'city': 0,
          'desired_age_from': 0,
          'desired_age_to': 0,
          'offset_for_search': 0}

headers = {
    'access_token': '2',
    'v': 0,
}


class TestVKMACHINERY(unittest.TestCase):
    def setUp(self):
        self.vk_machinery = VkMACHINERY()

    def tearDown(self):
        self.vk_machinery = None

    def test_arguments_in_users_search(self):
        with self.assertRaises(ValueError):
            self.vk_machinery.users_search(config, headers='2')
        with self.assertRaises(TypeError):
            self.vk_machinery.users_search(None, headers=headers)

        try:
            self.vk_machinery.users_search(config, headers)
        except KeyError:
            # that is ok because this method send request to VK API and get error response
            pass
        except (ValueError, TypeError):
            self.fail("vk_machinery.users_search() raised ExceptionType unexpectedly!")

    def test_arguments_in_get_processed_data_of_tinder_users(self):
        with self.assertRaises(TypeError):
            self.vk_machinery.get_processed_data_of_tinder_users(1)
            self.vk_machinery.get_processed_data_of_tinder_users(None)

        try:
            self.vk_machinery.get_processed_data_of_tinder_users([{'is_closed': True}])
        except KeyError:
            # that is ok because this method send request to VK API and get error response
            pass
        except (ValueError, TypeError):
            self.fail("vk_machinery.get_processed_data_of_tinder_users() raised ExceptionType unexpectedly!")


class TestTinderUsers(unittest.TestCase):
    def test_init_tinder_user(self):
        with self.assertRaises(TypeError):
            t = TinderUser([])
            t = TinderUser('')
            t = TinderUser(5)
            t = TinderUser(None)
        try:
            TinderUser()
        except BaseException:
            self.fail("vk_machinery.get_processed_data_of_tinder_users() raised ExceptionType unexpectedly!")


if __name__ == '__main__':
    unittest.main()
