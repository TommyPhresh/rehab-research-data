'''
Test nsf.gov data source
'''
import sys, os
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'
if c_path not in sys.path:
    sys.path.append(c_path)

import unittest
from unittest.mock import patch, Mock
import requests, json
from datetime import datetime

from scripts.pull_nsf import METADATA

MOCK_RESPONSE_HAPPY1 = {
    'response': {
        'award': [
            {
                'abstractText': "This project...",
                'awardeeName': 'Texas A&M Engineering Experiment Station',
                'id': '2532540',
                'expDate': '12/31/2029',
                'title': 'Collaborative Research: CISE-EPSRC: Efficient Constraint-Based Musculotendon Simulation for Biomechanically Accurate Characters'
            },
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
        ]
    }
}

MOCK_RESPONSE_HAPPY2 = {
    'response': {
        'award': [
            {
                'abstractText': "The project involves...",
                'awardeeName': 'San Francisco State University',
                'id': '2449902',
                'expDate': '06/30/2027',
                'title': 'CRII: HCC: RUI: AI-Driven Collaborative Goal Setting with Cognitively Assistive Robots'
            }
        ]
    }
}

class TestFetchData(unittest.TestCase):
    '''
    Tests happy path for fetch_data
    '''
    @patch('scripts.pull_nsf.requests.get')
    def test_fetch_data_happy(self, mock_get: Mock):
        # Configure mock objects
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = MOCK_RESPONSE_HAPPY1

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = MOCK_RESPONSE_HAPPY2

        mock_get.side_effect = [mock_response1, mock_response2]
        
        # Set params and call
        test_search_terms = ['test']
        test_last_refresh = '2024-03-14'
        result = METADATA['fetch_fn'](test_search_terms, test_last_refresh)

        # Checks
        expected = MOCK_RESPONSE_HAPPY1['response']['award']
        expected.extend(MOCK_RESPONSE_HAPPY2['response']['award'])
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_get.call_args_list[0].kwargs['params']['offset'], 1)
        self.assertEqual(mock_get.call_args_list[1].kwargs['params']['offset'], 26)
        params = mock_get.call_args_list[1].kwargs['params']
        self.assertEqual(params['rpp'], 25)
        self.assertEqual(params['keyword'], 'test')
        self.assertEqual(params['dateStart'], '03/14/2024')
        self.assertEqual(result, expected)

    '''
    Tests fetch_data ability to handle a HTTP error
    '''
    @patch('scripts.pull_nsf.requests.get')
    def test_fetch_data_http_error(self, mock_get: Mock):
        # Configure mock objects
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # Check
        result = METADATA['fetch_fn'](['test'], '2024-03-14')
        self.assertEqual(result, [])

    '''
    Tests fetch_data ability to handle empty response
    '''
    @patch('scripts.pull_nsf.requests.get')
    def test_fetch_data_empty_response(self, mock_get: Mock):
        # Configure mock objects
        mock_response_payload = {'response': {'award': []}}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_payload
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Check
        result = METADATA['fetch_fn'](['test'], '2024-03-14')
        self.assertEqual(result, [])

