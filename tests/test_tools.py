import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from screeninfo import Monitor

from src.tools import *


class TestTools(unittest.TestCase):
    def setUp(self):
        self.test_key_hash = hashlib.sha3_512('test_user'.encode('utf-8')).hexdigest()
        self.key_path_encrypted = b"943D9C2E5DB189D8'<\x8d\xc9,\xa3i\x82\xc1Up\x93\x16\x03\xde\xc1"
        self.site_path_encrypted = b'943D9C2E5DB189D8\x84%\xe0)\xd6\xef\xe0E]\xaf\x80\x106L\xdfR'
        self.test_key_path = 'test/key_path'
        self.test_site_path = 'test/site_path'
        self.test_dict = {
            '####1': hashlib.sha3_512('user_test'.encode('utf-8')).hexdigest().upper(),
            '####2': self.key_path_encrypted,
            '####3': self.site_path_encrypted
        }

    def tearDown(self):
        for file in Path('.').glob('*.bin'):
            file.unlink()

    def test_prefix_generator(self):
        self.assertIsInstance(prefix_generator(16), str)

    @patch('src.tools.os')
    def test_check_os(self, mock_os):
        mock_os.name = 'nt'
        self.assertEqual(check_os(), 'Windows')

    @patch('src.tools.os')
    def test_get_user_dir(self, mock_os):
        mock_os.name = 'nt'
        head, tail = get_user_dir()
        self.assertEqual(tail,  '/AppData/Local/PM/')

    @patch('src.tools.get_monitors')
    def test_display_info(self, mock_get_monitors):
        mock_get_monitors.return_value = [Monitor(x=1920, y=0, width=1920, height=1080, is_primary=True)]
        self.assertEqual(display_info(), (610.0, 315.0))

    @patch('src.tools.os.path')
    def test_users_list(self, mock_os_path):
        mock_os_path.isfile.return_value = True
        mock_open_result = mock_open(read_data='hash123')
        with patch('src.tools.open', mock_open_result):
            self.assertFalse(users_list('test_user'))

    def test_users_list_no_file(self):
        self.assertFalse(users_list('test_user'))

    @patch('src.tools.os.makedirs')
    @patch('src.tools.os.path')
    def test_create_users_list(self, mock_os_path, mock_os_makedirs):
        mock_os_path.exists.return_value = True
        mock_open_result = mock_open()
        with patch('src.tools.open', mock_open_result):
            create_users_list('test_user')
        mock_open_result.assert_called_once()

    @patch('src.tools.os.makedirs')
    @patch('src.tools.get_user_dir')
    def test_store_directory_paths(self, mock_user_dir, mock_os_makedirs):
        mock_user_dir.return_value = '', ''
        store_directory_paths('test_user', self.test_key_path, self.test_site_path, self.test_key_hash)
        with open('500BAB86E4E022E5.bin', 'r') as f:
            first_line = f.readline()
            path = eval(first_line)
            self.assertEqual(path['####1'], self.test_key_hash.upper())

    @patch('src.tools.os.path')
    @patch('src.tools.get_user_dir')
    def test_fetch_directory_paths(self, mock_user_dir, mock_path):
        with open('943D9C2E5DB189D8.bin', 'w') as f:
            f.write(str(self.test_dict))
        mock_user_dir.return_value = '', ''
        mock_path.exists.return_value = True
        key_path, site_path = fetch_directory_paths('user_test')
        self.assertEqual(key_path.decode('utf-8'), self.test_key_path)
        self.assertEqual(site_path.decode('utf-8'), self.test_site_path)

    def test_fetch_directory_path_nonexistent_user(self):
        self.assertFalse(fetch_directory_paths('nonexistent_user'))

    @patch('src.tools.get_user_dir')
    @patch('src.tools.fetch_directory_paths')
    @patch('src.tools.os.remove')
    def test_delete_files(self, mock_os_remove, mock_fetch_directory_paths, mock_user_dir):
        with open('G4OP28duO04S5r96.bin', 'w') as f:
            f.write(hashlib.sha3_512('test'.encode('utf-8')).hexdigest().upper())
        with open('9ECE086E9BAC491F.bin', 'w') as f:
            pass
        mock_user_dir.return_value = '', ''
        mock_fetch_directory_paths.return_value = ('key_path', 'site_path')
        delete_files('test')
        assert 3 == mock_os_remove.call_count
        mock_os_remove.assert_called_with('9ECE086E9BAC491F.bin')
