'''
Test grants.gov data source
'''
import sys, os
# The path to packages on the C: drive
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if c_path not in sys.path:
    sys.path.append(c_path)

import unittest
from unittest.mock import patch, Mock
import json, requests
from datetime import datetime

from scripts.pull_grants import fetch_data, transform_data

class TestTransformData(unittest.TestCase):
    '''
    Test transform_data happy path
    '''
    def test_transform_data_happy(self):
        raw_data = [MOCK_HAPPY_PATH]
        expected_result = {
            "name": "value",
            "org": "value",
            "desc": "value",
            "deadline": "value",
            "link": "value",
            "isGrant": True
        }
        self.assertEqual(transform_data(raw_data), expected_result)

    '''
    Test transform_data edge case: if needed 
    '''

    '''
    Test transform_data edge case: empty data
    '''
    def test_transform_data_empty(self):
        self.assertEqual(transform_data([]), [])


class TestFetchData(unittest.TestCase):
    '''
    Test fetch_data happy path
    '''
    @patch('scripts.pull_grants.requests.post')
    def test_fetch_data_happy(self, mock_post: Mock):
        mock_response_payload = {}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_payload
        mock_post.return_value = mock_response

        expected_result = []
        result = fetch_data(arg1, ['search term'], '2025-01-01')

        mock_get.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], API_URL)
        params = kwargs['params']
        self.assertIn("desired param", params)
        self.assertEqual(params['desired check'], '2025-01-01')
        self.assertEqual(result, expected_result)

    '''
    Test fetch_data edge case: HTTP error
    '''
    @patch('scripts.pull_grants.requests.post')
    def test_fetch_data_http_error(self, mock_post: Mock):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_post.return_value = mock_response

        result = fetch_data(arg1, ['search term'], '2025-01-01')
        self.assertEqual(result, [])

    '''
    Test fetch_data edge case: empty response
    '''
    @patch('scripts.pull_grants.requests.post')
    def test_fetch_data_empty(self, mock_post: Mock):
        mock_response_payload = {}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_payload
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = fetch_data(arg1, ['search term'], '2025-01-01')
        self.assertEqual(result, [])
        
