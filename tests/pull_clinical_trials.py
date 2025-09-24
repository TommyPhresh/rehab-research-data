'''
This file tests all functions within pull_clinical_trials.py.
It uses a Mock object s.t. we can test without actually creating/deleting 
files. 
'''

import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import os
import sys

from scripts.pull_clinical_trials import get_last_refresh, update_last_refresh, fetch_data, save_raw_data, LAST_PULL_DATE_FILE

# The path to packages on the C: drive
requests_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if requests_path not in sys.path:
    sys.path.append(requests_path)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestRefreshFunctions(unittest.TestCase):
    # Tear down mock object every test for a clean call history
    def setUp(self):
        self.patcher = patch('scripts.pull_clinical_trials.open', 
                             new_callable=mock_open)
        self.mock_file = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.mock_file.reset_mock()


    '''
    `test_update_last_refresh` ensures that `LAST_PULL_DATE_FILE` properly 
    refreshes using the current date.
    '''
    def test_update_last_refresh(self):
        expected_date = datetime.now().strftime("%Y-%m-%d")
        update_last_refresh()
        self.mock_file.assert_called_with(LAST_PULL_DATE_FILE, "w")
        self.mock_file().write.assert_called_once_with(expected_date)

    '''
    `test_get_last_refresh_file_exists` ensures that `get_last_refresh` is 
    called using `LAST_PULL_DATE_FILE` and the correct information is 
    retrieved.
    '''
    def test_get_last_refresh_file_exists(self):
        self.mock_file().read.return_value= "2024-01-01"
        date = get_last_refresh()
        self.assertEqual(date, "2024-01-01")
        self.mock_file.assert_called_with(LAST_PULL_DATE_FILE, "r")

    '''
    `test_get_last_refresh_no_file` ensures that `get_last_refresh` returns
    the default "date minimum" when no file is found.
    '''
    def test_get_last_refresh_no_file(self):
        self.mock_file.side_effect = FileNotFoundError
        date = get_last_refresh()
        self.assertEqual(date, "1900-01-01")


if __name__ == "__main__GIT_SSH_COMMAND='ssh -i ~/.ssh/id_rsa_personal' git push origin main":
    unittest.main()


