'''
This file tests all functions within pull_clinical_trials.py.
It uses a Mock object s.t. we can test without actually creating/deleting 
files. 
'''

import unittest, os, sys, json
from unittest.mock import patch, mock_open, Mock, MagicMock
from datetime import datetime

from scripts.pull_clinical_trials import main, get_last_refresh, update_last_refresh, fetch_data, save_raw_data, read_jsonl_file, transform_data, LAST_PULL_DATE_FILE, API_URL, PAGE_SIZE, SEARCH_TERMS, RAW_DATA_PATH
from tests.mock_data_clinical_trials import MOCK_API_RESPONSE_SINGLE_PAGE, MOCK_API_RESPONSE_MULTI_PAGE_1, MOCK_API_RESPONSE_MULTI_PAGE_2, MOCK_API_RESPONSE_SUPER_HAPPY, MOCK_API_RESPONSE_NO_PRIMARY_DATE, MOCK_API_RESPONSE_NO_ORG, MOCK_API_RESPONSE_SHITTY_DATA, MOCK_JSONL_CONTENT, MOCK_API_RESPONSE_MAIN, EXPECTED_TRANSFORMED_DATA

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

class TestFetchData(unittest.TestCase):

    '''
    `test_get_one_page_happy` ensures `fetch_page` can correctly handle a 
    successful API one-page response.
    '''
    @patch('requests.get')
    def test_get_one_page_happy(self, mock_get): 
        # Configure mock file to simulate successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_API_RESPONSE_SINGLE_PAGE

        # Fake it til you make it
        mock_get.return_value = mock_response
        studies = fetch_data('conditions', 'rehabilitation', '1900-01-01')
        
        # Check assertions
        mock_get.assert_called_once_with(
            API_URL, 
            params={
                'format': 'json',
                'query.locs': 'United States',
                'filter.overallStatus': 'RECRUITING|NOT_YET_RECRUITING|ACTIVE_NOT_RECRUITING|ENROLLING_BY_INVITATION',
                'pageSize': PAGE_SIZE,
                'filter.lastRefreshPostDate': '1900-01-01',
                'query.cond': 'rehabilitation'
                }
            )
        self.assertEqual(len(studies), 1)
        self.assertEqual(studies[0]['protocolSection']['sponsorCollaboratorsModule']['leadSponsor']['name'], 'Acme Pharmaceuticals')
        self.assertIsInstance(studies, list)
        self.assertIsInstance(studies[0], dict)

    '''
    `test_get_multi_page_happy` ensures `fetch_page` can correctly handle a 
    successful API multi-page response.
    '''
    @patch('requests.get')
    def test_get_multi_page_happy(self, mock_get):
        # Configure mock file to simulate successful API response
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = MOCK_API_RESPONSE_MULTI_PAGE_1
        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = MOCK_API_RESPONSE_MULTI_PAGE_2

        # Fake it til you make it 
        mock_get.side_effect = [mock_response1, mock_response2]
        studies = fetch_data('conditions', 'imaginary condition', '1900-01-01')

        # Check assertions
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(len(studies), 2)
        fake_ids = [study['protocolSection']['identificationModule']['nctId'] for study in studies]
        self.assertIn('NCT00000002', fake_ids)
        self.assertIn('NCT00000003', fake_ids)

    '''
    `test_fetch_page_error` ensures `fetch_page` can correctly handle an unsuccessful API response.
    '''
    @patch('requests.get')
    def test_fetch_page_error(self, mock_get):
        # Configure mock file to simulate unsuccessful API response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        # Fake that hoe
        mock_get.return_value = mock_response
        with patch('builtins.print') as mock_print:
            studies = fetch_data('conditions', 'brain tumors', '1900-01-01')

        # Check assertions
        mock_get.assert_called_once()
        self.assertEqual(studies, [])
        mock_print.assert_called_with('Error: Internal Server Error')

class TestSaveRawData(unittest.TestCase):
    '''
    Ensures `save_raw_data` correctly writes JSON data to the designated save file.
    '''
    @patch('scripts.pull_clinical_trials.open', new_callable=mock_open)
    def test_save_raw_data_happy(self, mock_file):
        # Configure mock files
        fake_data = [{'NCTId':'NCT001', 'title':'Number One'},
                     {'NCTId':'NCT002', 'title':'Number Two'}]
        save_raw_data(fake_data)
        
        # Check assertions
        mock_file.assert_called_with(RAW_DATA_PATH, 'w')
        expected_content_list = [json.dumps(item) for item in fake_data]
        expected_content = '\n'.join(expected_content_list) + '\n'
        all_args = mock_file.return_value.write.call_args_list
        actual_content = ''.join(arg[0][0] for arg in all_args)
        self.assertEqual(actual_content, expected_content)

class TestReadData(unittest.TestCase):
    '''
    Ensures `read_jsonl_file` correctly reads JSONL data from designated save file.
    '''
    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_JSONL_CONTENT)
    def test_read_jsonl_happy(self, mock_file_open):
        expected_data = [{'id': 'study1', 'data': 'A'},
                         {'id': 'study2', 'data': 'B'}]
        with patch('os.path.exists', return_value=True):
            actual_data = read_jsonl_file(RAW_DATA_PATH)
        self.assertEqual(actual_data, expected_data)
        mock_file_open.assert_called_with(RAW_DATA_PATH, 'r')

    '''
    Ensures `read_jsonl_file` can handle a missing file.
    '''
    @patch('builtins.print')
    @patch('os.path.exists', return_value=False)
    def test_read_jsonl_file_missing_file(self, mock_exists, mock_print):
        actual_data = read_jsonl_file(RAW_DATA_PATH)
        self.assertEqual(actual_data, [])
        self.assertIn('does not exist.', mock_print.call_args[0][0])

    '''
    Ensures `read_jsonl_file` can handle a corrupted file.
    '''
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open, read_data = "{'id': 'study1', 'DELETE TABLE IF EXISTS}")
    def test_read_jsonl_file_corrupted_file(self, mock_file_open, mock_print):
        with patch('os.path.exists', return_value=True):
            actual_data = read_jsonl_file(RAW_DATA_PATH)
        self.assertEqual(actual_data, [])
        mock_print.assert_called_once()
        self.assertIn('Error decoding JSON:', mock_print.call_args[0][0])


class TestDataTransform(unittest.TestCase):
    '''
    Ensures that `transform_data` correctly converts from clinicaltrials
    API format to rehab-research universal format, using highest-priority values
    for `org` and `deadline`.
    '''
    def test_transform_data_super_happy(self):
        expected_transformed_data = [{
            'name': 'A Phase III Trial for New Immunotherapy Drug',
            'org': 'Global Pharma Research Institute',
            'desc': 'This study aims to assess the efficacy and safety of a novel immunotherapy drug in patients with advanced cancer.',
            'deadline': '2025-09-25',
            'link': 'https://clinicaltrials.gov/study/NCT00000001',
            'isGrant': False
        }]
        actual_transformed_data = transform_data(MOCK_API_RESPONSE_SUPER_HAPPY)

        self.assertEqual(actual_transformed_data, expected_transformed_data)

    '''
    Ensures that `transform_data` correctly converts to universal format when sponsor not present.
    '''
    def test_transform_data_no_sponsor(self):
        expected_transformed_data = [{
            'name': 'A Study of Gene Therapy in Pediatric Patients',
            'org': 'Pediatric Health Consortium',
            'desc': 'Investigating a novel gene therapy approach.',
            'deadline': '2024-12-31',
            'link': 'https://clinicaltrials.gov/study/NCT00000002',
            'isGrant': False
        }]
        actual_transformed_data = transform_data(MOCK_API_RESPONSE_NO_ORG)
        self.assertEqual(actual_transformed_data, expected_transformed_data)

    '''
    Ensures that `transform_data` correctly converts to universal format when primary date not present.
    '''
    def test_transform_data_no_primary_date(self):
        expected_transformed_data = [{
            'name': 'Dietary Intervention for Metabolic Syndrome',
            'org': 'Academic Medical Center',
            'desc': 'Assessing the impact of a low-carb diet on patients with metabolic syndrome.',
            'deadline': '2027-06-15',
            'link': 'https://clinicaltrials.gov/study/NCT00000003',
            'isGrant': False
        }]
        actual_transformed_data = transform_data(MOCK_API_RESPONSE_NO_PRIMARY_DATE)
        self.assertEqual(actual_transformed_data, expected_transformed_data)

    '''
    Ensures that `transform_data` handles when both org and deadline priority values missing.
    '''
    def test_transform_data_no_priority_vals(self):
        expected_transformed_data = [{
            'name': 'A Study with Minimal Information',
            'org': 'No organization listed',
            'desc': 'This summary is present.',
            'deadline': '9999-12-31',
            'link': '',
            'isGrant': False
        }]
        actual_transformed_data = transform_data(MOCK_API_RESPONSE_SHITTY_DATA)
        self.assertEqual(actual_transformed_data, expected_transformed_data)

class TestMain(unittest.TestCase):
    '''
    Tests that the `main()` function of `pull_clinical_trials` script performs a full data pull correctly.
    '''
    @patch('scripts.pull_clinical_trials.update_last_refresh')
    @patch('scripts.pull_clinical_trials.save_raw_data')
    @patch('scripts.pull_clinical_trials.fetch_data')
    @patch('scripts.pull_clinical_trials.get_last_refresh')
    def test_main_full(self, mock_get_last_refresh, mock_fetch_data, 
                       mock_save_raw_data, mock_update_last_refresh):
        # Configure mock files
        mock_get_last_refresh.return_value = '1900-01-01'
        mock_fetch_data.return_value = [{'NCTId':'NCT001'}, {'NCTId': 'NCT002'}]
        expected_numcalls = len(SEARCH_TERMS['conditions']) + len(SEARCH_TERMS['interventions'])
        main()

        # Check assertions
        mock_get_last_refresh.assert_called_once()
        self.assertEqual(mock_fetch_data.call_count, expected_numcalls)
        mock_save_raw_data.assert_called_once()
        studies = mock_save_raw_data.call_args[0][0]    
        self.assertEqual(len(studies), 2*expected_numcalls)
        mock_update_last_refresh.assert_called_once()

    ''' 
    Tests that the `main()` function of `pull_clinical_trials` script correctly handles incremental data pull (only updates, not the whole thing again)
    '''
    @patch('scripts.pull_clinical_trials.update_last_refresh')
    @patch('scripts.pull_clinical_trials.save_raw_data')
    @patch('scripts.pull_clinical_trials.fetch_data')
    @patch('scripts.pull_clinical_trials.get_last_refresh')
    def test_main_incremental(self, mock_get_last_refresh, mock_fetch_data,
                       mock_save_raw_data, mock_update_last_refresh):
        # Configure mock files
        expected_numcalls = len(SEARCH_TERMS['conditions']) + len(SEARCH_TERMS['interventions'])
        yesterday = '2025-09-24'
        mock_get_last_refresh.return_value = yesterday
        mock_fetch_data.return_value = [{'NCTId':'NCT001'}, {'NCTId':'NCT002'}]
        main()

        # Check assertions
        mock_get_last_refresh.assert_called_once()
        self.assertEqual(mock_fetch_data.call_count, expected_numcalls)
        for call in mock_fetch_data.call_args_list:
            call_posargs = call[0]
            self.assertEqual(call_posargs[2], yesterday)
        mock_save_raw_data.assert_called_once()
        studies = mock_save_raw_data.call_args[0][0]
        self.assertEqual(len(studies), 2*expected_numcalls)
        mock_update_last_refresh.assert_called_once()

    # Hold data for integration test
    mock_file_handle = mock_open()

    '''
    Tests `main()` function start to finish. Assumes all components of `main`
    work correctly, only tests logical flow.
    '''
    @patch('scripts.pull_clinical_trials.requests.get')
    @patch('scripts.pull_clinical_trials.get_last_refresh', return_value='2025-09-26')
    @patch('scripts.pull_clinical_trials.update_last_refresh')
    @patch('scripts.pull_clinical_trials.os.path.exists', return_value=True)
    @patch('scripts.pull_clinical_trials.to_universal_format')
    @patch('scripts.pull_clinical_trials.RAW_DATA_PATH', new='directory/raw.jsonl')
    @patch('scripts.pull_clinical_trials.open', new_callable=lambda: TestMain.mock_file_handle)
    def test_main_integration(self, mock_open,
                              mock_to_universal_format, mock_exists,
                              mock_update_last_refresh, mock_get_last_refresh,
                              mock_get):
        # Configure mock files
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_API_RESPONSE_MAIN
        mock_get.return_value = mock_response
        mock_to_universal_format.return_value = EXPECTED_TRANSFORMED_DATA
        raw_data = json.dumps(MOCK_API_RESPONSE_MAIN['studies'][0]) + '\n'
        TestMain.mock_file_handle.return_value.readlines.return_value = [raw_data]

        # Go
        main()

        # Check assertions
        self.assertTrue(mock_get.called)
        save_raw_data_call = [c for c in mock_open.call_args_list if c.args[1] == 'w'][0]
        self.assertIn('directory/raw.jsonl', save_raw_data_call.args[0])
        self.assertTrue(mock_update_last_refresh.called)
        mock_to_universal_format.assert_called_with('directory/raw.jsonl')


if __name__ == '__main__':
    unittest.main()


