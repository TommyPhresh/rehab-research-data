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
from scripts.pipeline_conductor import main as pipeline_main

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

class TestToUniversalFormat(unittest.TestCase):
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

class TestPipelineConductor(unittest.TestCase):
    '''
    Test pipeline is in correct sequence and functions happily
    '''
    @patch('scripts.pipeline_conductor.get_last_refresh', return_value='2024-03-14')
    @patch('scripts.pipeline_conductor.save_raw_data')
    @patch('scripts.pipeline_conductor.update_last_refresh')
    @patch('requests.get')
    @patch('requests.post')
    @patch('scripts.pipeline_conductor.SOURCE_REGISTRY')
    @patch('scripts.utils.read_jsonl_file', return_value=MOCK_RAW_DATA)
    @patch('scripts.pipeline_conductor.save_processed_data')
    def test_pipeline_correct_sequence(self,
                                       mock_save_processed_data,
                                       mock_read_jsonl_file,
                                       mock_SOURCE_REGISTRY,
                                       mock_post,
                                       mock_get,
                                       mock_update_last_refresh,
                                       mock_save_raw_data, 
                                       mock_get_last_refresh):
        local_fetch = MagicMock(return_value=MOCK_RAW_DATA)
        local_transform = MagicMock(side_effect=lambda data: [f'transform_{d["id"]}' for d in data])

        local_metadata = {
            'name': 'mock', 
            'search_terms': ['test', 'search'],
            'fetch_fn': local_fetch,
            'transform_fn': local_transform,
            'raw_path': 'directory/raw.jsonl'
        }
        mock_SOURCE_REGISTRY.__iter__.return_value = [local_metadata]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.raise_for_status = None
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        local_metadata['fetch_fn'].reset_mock()
        
        results = pipeline_main()        

        mock_get_last_refresh.assert_called_once()
        local_metadata['fetch_fn'].assert_called_with(
            local_metadata['search_terms'],
            '2024-03-14'
        )
        
        mock_save_raw_data.assert_called_with(
            MOCK_RAW_DATA,
            local_metadata['raw_path']
        )

        mock_read_jsonl_file.assert_called_with(local_metadata['raw_path'])
        local_metadata['transform_fn'].assert_called_with(MOCK_RAW_DATA)

        expected_transformed = ['transform_BULL', 'transform_CRAP'] * 2
        mock_save_processed_data.assert_called_with(
                expected_transformed,
                'data/processed/unvectorized.jsonl')
        
        mock_update_last_refresh.assert_called_once()
        
