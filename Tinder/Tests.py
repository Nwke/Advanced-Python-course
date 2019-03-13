from Tinder import VkMACHINERY
from Tinder.TinderUsers import TinderUser, MainUser

import sys
import unittest


class TestVKMACHINERY(unittest.TestCase):
    def setUp(self):
        self.vk_machinery = VkMACHINERY()
        self.old_stdin = sys.stdin
        self.config = {'count_for_search': 0,
                       'sex': 0,
                       'city': 0,
                       'desired_age_from': 0,
                       'desired_age_to': 0,
                       'offset_for_search': 0}
        self.headers = {
            'access_token': '2',
            'v': 0,
        }

    def tearDown(self):
        self.vk_machinery = None

    def test_arguments_in_users_search(self):
        with self.assertRaises(ValueError):
            self.vk_machinery.users_search(self.config, headers='2')
        with self.assertRaises(TypeError):
            self.vk_machinery.users_search(None, headers=self.headers)

        try:
            self.vk_machinery.users_search(self.config, self.headers)
        except KeyError:
            # that is ok because this method send request to VK API and get error response
            pass
        except (ValueError, TypeError):
            self.fail("vk_machinery.users_search() raised ExceptionType unexpectedly!")

    def test_search_user(self):
        try:
            main_user = MainUser(DEBUG=True)
            main_user_config = main_user.get_search_config_obj()
            main_user_request_headers = main_user._get_headers()

            res = self.vk_machinery.users_search(main_user_config, main_user_request_headers)
            self.assertEqual(type(res), type(list()), 'Result must have a type like list')
        except BaseException:
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
        except TypeError:
            self.fail("vk_machinery.get_processed_data_of_tinder_users() raised TypeError unexpectedly!")


class TestTinderUser(unittest.TestCase):
    def test_init_tinder_user(self):
        with self.assertRaises(TypeError):
            t = TinderUser([])
            t = TinderUser('')
            t = TinderUser(5)
            t = TinderUser(None)
        try:
            TinderUser()
        except BaseException:
            self.fail("Create TinderUser() raised anyException unexpectedly!")


if __name__ == '__main__':
    unittest.main()
