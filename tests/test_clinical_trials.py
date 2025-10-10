'''
Test clinicaltrials.gov data source
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

from scripts.pull_clinical_trials import fetch_data, transform_data, API_URL, SEARCH_TERMS

MOCK_HAPPY_PATH = {
    "protocolSection": {
        "identificationModule": {
            "nctId": "NCT01234567",
            "briefTitle": "Introducing Palliative Care (PC) Within the Treatment of End Stage Liver Disease (ESLD)",
            "organization": {
                "fullName": "Budweiser"
            }
        },
        "statusModule": {
            "overallStatus": "RECRUITING",
            "primaryCompletionDateStruct": {
                "date": "2026-09-30"
            },
            "completionDateStruct": {
                "date": "2025-10-03"
            },
            "lastUpdatePostDateStruct": {
                "date": "2025-05-01"
            },
        },
        "sponsorCollaboratorsModule": {
            "leadSponsor": {
                "name": "Coors Light"
            }
        },
        "descriptionModule": {
            "briefSummary": "We are looking to investigate the efficacy of a PC driven treatment for ESLD on patient and family outcomes",
            "detailedDescription": "Not the right answer"
        }
    }
}

MOCK_FALLBACK = {
    "protocolSection": {
        "identificationModule": {
            "nctId": "NCT012344444",
            "organization": {
                "fullName": "Mr. Clean"
            }
        },
        "statusModule": {
            "overallStatus": "RECRUITING"
        },
        "completionDateStruct": {
            "date": "2025-10-03"
        },
        "descriptionModule": {
            "briefSummary": "We are looking to investigate the efficacy of a PC driven treatment for ESLD on patient and family outcomes",
            "detailedDescription": "Not the right answer"
        },
    }
}

MOCK_CORRUPTED = {
    "protocolSection": {
        "identificationModule": {
            "organization": {
            }
        },
        "statusModule": {
            "overallStatus": "RECRUITING"
        },
        "primaryCompletionDateStruct": {
            "date": "01/01/2013"
        },
    }
}

class TestTransformData(unittest.TestCase):
    '''
    Tests transform_data function logic.
    '''
    def test_transform_happy(self):
        raw_data = [MOCK_HAPPY_PATH]
        expected_record = {
            "name": "Introducing Palliative Care (PC) Within the Treatment of End Stage Liver Disease (ESLD)",
            "org": "Coors Light",
            "desc": "We are looking to investigate the efficacy of a PC driven treatment for ESLD on patient and family outcomes",
            "deadline": "2026-09-30",
            "link": "https://clinicaltrials.gov/study/NCT01234567",
            "isGrant": False
        }
        self.assertEqual(transform_data(raw_data), [expected_record])

    '''
    Tests transform_data fallback logic
    '''
    def test_transform_fallback(self):
        raw_data = [MOCK_FALLBACK]
        expected_record = {
            "name": "No name given",
            "org": "Mr. Clean",
            "desc": "We are looking to investigate the efficacy of a PC driven treatment for ESLD on patient and family outcomes",
            "deadline": "9999-12-31",
            "link": "https://clinicaltrials.gov/study/NCT012344444",
            "isGrant": False
        }
        self.assertEqual(transform_data(raw_data), [expected_record])

    '''
    Tests transform_data corruption handling
    '''
    def test_transform_corrupt(self):
        raw_data = [MOCK_CORRUPTED]
        expected_record = {
            "name": "No name given",
            "org": "No organization listed",
            "desc": "No description given",
            "deadline": "9999-12-31",
            "link": "",
            "isGrant": False
        }
        self.assertEqual(transform_data(raw_data), [expected_record])

    '''
    Tests transform_data on empty list
    '''
    def test_transform_empty(self):
        self.assertEqual(transform_data([]), [])

            
class TestFetchData(unittest.TestCase):
    '''
    Tests happy path for fetch_data
    '''
    @patch('scripts.pull_clinical_trials.requests.get')
    def test_fetch_data_happy(self, mock_get: Mock):
        # configure mock objects
        mock_response_payload = {
            "studies": [
                {
                    "protocolSection": {
                        "identificationModule": {
                            "nctId": "NCT01234567",
                            "briefTitle": "Introducing Palliative Care (PC) Within the Treatment of End Stage Liver Disease (ESLD)",
                            "organization": {
                                "fullName": "Budweiser"
                            }
                        },
                        "statusModule": {
                            "overallStatus": "RECRUITING",
                            "primaryCompletionDateStruct": {
                                "date": "2026-09-30"
                            },
                            "completionDateStruct": {
                                "date": "2025-10-03"
                            },
                            "lastUpdatePostDateStruct": {
                                "date": "2025-05-01"
                            },
                        },
                        "sponsorCollaboratorsModule": {
                            "leadSponsor": {
                                "name": "Coors Light"
                            }
                        },
                        "descriptionModule": {
                            "briefSummary": "We are looking to investigate the efficacy of a PC driven treatment for ESLD on patient and family outcomes",
                            "detailedDescription": "Not the right answer"
                        }
                    }
                }
            ]
        }
        # Configure mock objects           
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_payload
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # set params and 'correct' answer
        expected_result = [mock_response_payload['studies'][0]] * 2

        test_search_terms = {'conditions': ['test'], 'interventions': ['test2']}
        test_last_refresh = "2025-01-01"
        result = fetch_data(test_search_terms, test_last_refresh)

        # checks
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], API_URL)
        params = kwargs['params']
        self.assertIn('query.cond', params)
        self.assertIn('sort', params)
        self.assertEqual(result, expected_result)

    '''
    Tests fetch_data ability to handle an HTTP error
    '''
    @patch('scripts.pull_clinical_trials.requests.get')
    def test_fetch_data_http_error(self, mock_get: Mock):
        # configure mock objects
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # check
        result = fetch_data({'conditions': ['test'], 'interventions': ['test2']}, '2025-01-01')
        self.assertEqual(result, [])

    '''
    Tests fetch_data ability to handle an empty list of studies
    '''
    @patch('scripts.pull_clinical_trials.requests.get')
    def test_fetch_data_no_results(self, mock_get: Mock):
        mock_response_payload = {'studies': []}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_payload
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_data({'conditions': ['test'], 'interventions': ['test2']}, '2025-01-01')
        self.assertEqual(result, [])
        
