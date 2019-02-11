import unittest
import Tests.src.helpers.config as config

from Tests.src.helpers.config import WINDOWS, APP_NAME

test_cfg = config.Config()


class TestApp(unittest.TestCase):
    def setUp(self):
        self.test_cfg = config.Config()
        
        self.init_env_in_windows_part_cases = ['.\\', 'C:\\']
        self.init_env_in_not_windows_part_cases = ['./', '~/', '~/.{}'.format(APP_NAME), '/etc/{}'.format(APP_NAME)]

    def tearDown(self):
        self.test_cfg = None

    def test_verbosity_level(self):
        levels = self.test_cfg.get_verbosity_level()
        self.assertEqual(levels, 'critical, error, warning, info, debug', 'test_verbosity_level failed')

        value = test_cfg.get_verbosity_level(level='console')
        self.assertEqual(value, 10)

        value = test_cfg.get_verbosity_level(level='error')
        self.assertEqual(value, 40)

    def test_get_windows_system_disk(self):
        if WINDOWS:
            path_system_disk = test_cfg.get_windows_system_disk()
            self.assertEqual(path_system_disk, 'C:', 'test system disk failed')
        else:
            self.assertRaises(EnvironmentError)

    def test_init_env_config_path(self):
        if WINDOWS:
            all_elements_in_init_env_in_windows = self.test_cfg.init_env_config_path()
            for required_elements_in_env_init in self.init_env_in_windows_part_cases:
                self.assertIn(required_elements_in_env_init, all_elements_in_init_env_in_windows)
        else:
            all_elements_in_init_env_not_windows = self.test_cfg.init_env_config_path()
            for required_elements_in_env_init in self.init_env_in_not_windows_part_cases:
                self.assertIn(required_elements_in_env_init, all_elements_in_init_env_not_windows)

    def test_init_config(self):
        self.assertIsNotNone(self.test_cfg.config_file)
        self.assertIsNotNone(self.test_cfg.config_paths)


if __name__ == '__main__':
    unittest.main()
