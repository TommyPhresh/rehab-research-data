'''
Test overall pipeline structure
'''
import sys, os
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'
if c_path not in sys.path:
    sys.path.append(c_path)

import unittest, json
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

from scripts.utils import (get_last_refresh, update_last_refresh,
                           save_raw_data, read_jsonl_file, to_universal_format)

DEFAULT_DATE = '1900-01-01'
MOCK_DATE_PATH = 'data/last_pull_date.txt'
MOCK_RAW_DATA_PATH = 'data/raw/clinical_trials.jsonl'
MOCK_RAW_DATA = [
    {'id': "BULL"}, {'id': "CRAP"}
]

class TestRefresh(unittest.TestCase):
    '''
    Tests get_last_refresh happy path
    '''
    @patch('scripts.utils.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=DEFAULT_DATE)
    def test_get_last_refresh_happy(self, mock_file, mock_exists):
        date = get_last_refresh()
        mock_file.assert_called_with(MOCK_DATE_PATH, 'r')
        self.assertEqual(date, DEFAULT_DATE)

    '''
    Tests get_last_refresh edge case: file not found
    '''
    @patch('scripts.utils.os.path.exists', return_value=False)
    def test_get_last_refresh_no_file(self, mock_exists):
        date = get_last_refresh()
        self.assertEqual(date, DEFAULT_DATE)

    '''
    Tests update_last_refresh happy path
    '''
    @patch('scripts.utils.datetime')
    @patch('builtins.open', new_callable=mock_open)
    def test_update_last_refresh_happy(self, mock_file, mock_datetime):
        mock_datetime.now.return_value = datetime(2025,10,3)
        update_last_refresh()
        expected_date = '2025-10-03'
        mock_file.assert_called_with(MOCK_DATE_PATH, 'w')
        mock_file().write.assert_called_with(expected_date)

class TestIOLogic(unittest.TestCase):
    '''
    Tests save_raw_data happy path
    '''
    @patch('builtins.open', new_callable=mock_open)
    def test_save_raw_data_happy(self, mock_file):
        save_raw_data(MOCK_RAW_DATA, MOCK_RAW_DATA_PATH)
        mock_file.assert_called_with(MOCK_RAW_DATA_PATH, 'w')
        saved_data = "".join([call[0][0] for call in mock_file().write.call_args_list])
        expected_data = ""
        for item in MOCK_RAW_DATA:
            expected_data += json.dumps(item) + "\n"
        self.assertEqual(saved_data, expected_data)
    
    '''
    Tests read_jsonl_file happy path
    '''
    @patch('scripts.utils.os.path.exists', return_value=True)
    def test_read_jsonl_file_happy(self, mock_exists):
        file_content = (json.dumps(MOCK_RAW_DATA[0]) + '\n' +
                        json.dumps(MOCK_RAW_DATA[1]) + '\n')
        with patch('builtins.open', mock_open(read_data=file_content)) as mock_file:
            data = read_jsonl_file(MOCK_RAW_DATA_PATH)
        mock_file.assert_called_with(MOCK_RAW_DATA_PATH, 'r')
        self.assertEqual(data, MOCK_RAW_DATA)

    '''
    Test read_jsonl_file edge case: file not found
    '''
    @patch('scripts.utils.os.path.exists', return_value=False)
    def test_read_jsonl_file_no_file(self, mock_exists):
        data = read_jsonl_file(MOCK_RAW_DATA_PATH)
        self.assertEqual(data, [])

class TestPipelineConductor(unittest.TestCase):
    '''
    Universal mock transform_data function
    '''
    def mock_transform_data(self, raw_data):
        return [f"Transformed_{r['id']}" for r in raw_data]

    '''
    Tests to_universal_format happy path
    '''
    @patch('scripts.utils.read_jsonl_file')
    def test_to_universal_format_happy(self, mock_read):
        mock_read.return_value = MOCK_RAW_DATA
        processed_data = to_universal_format(MOCK_RAW_DATA_PATH, self.mock_transform_data)
        mock_read.assert_called_with(MOCK_RAW_DATA_PATH)
        self.assertEqual(processed_data, ["Transformed_BULL", "Transformed_CRAP"])

    '''
    Tests to_universal_format edge case: no data to transform
    '''
    @patch('scripts.utils.read_jsonl_file', return_value=[])
    def test_to_universal_format_no_data(self, mock_read):
        processed_data = to_universal_format(MOCK_RAW_DATA_PATH, self.mock_transform_data)
        self.assertEqual(processed_data, [])
