'''
This file efficiently handles incremental pulls from nsf.gov.
Uses a list of terms to pull relevant and new/updated data.
'''
import sys, os
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'
if c_path not in sys.path: 
    sys.path.append(c_path)

import requests, json
from datetime import datetime

API_URL = 'http://api.nsf.gov/services/v1/awards.json'
SEARCH_TERMS = [
    "Interventional Spine", "Pain Management", "Electromyography", "Electrodiagnostics", "Radiculopathy",
    "Musculoskeletal Rehabilitation", "Ultrasound", "Pediatric Rehabilitation", "Neuropsychology",
    "Rehabilitation Psychology", "Traumatic Brain Injury", "Stroke Rehabilitation", "Spasticity",
    "Physical Therapy", "Occupational Therapy", "Rehabilitation", "Limb Loss",
]
ROWS_PER_PAGE = 25
RAW_DATA_PATH = 'data/raw/nsf.jsonl'

'''
Returns results across all search terms
(list[str], str) -> list[dict]
Params:
    `terms: list[str]`. List of all search terms for nsf.gov.
    `last_refresh: str`. YYYY-MM-DD formatted string representing last successful pull.
'''
def fetch_data(terms, last_refresh):
    try:
        last_refresh_datetime = datetime.strptime(last_refresh, "%Y-%m-%d").date()
    except ValueError:
        last_refresh_datetime = datetime(1900,1,1).date()

    all_results = []
    offset = 1
    query = " OR ".join(terms)
    while True:
        params = {
            'dateStart': datetime.strftime(last_refresh_datetime, "%m/%d/%Y"),
            'offset': offset,
            'printFields': 'id,title,abstractText,awardeeName,expDate',
            'keyword': query,
            'rpp': ROWS_PER_PAGE,
            'agency': 'NSF'
        }
        try:
            print(offset)
            response = requests.get(API_URL, params=params)
        
            if response.status_code != 200:
                print(f"Error: {response.text}")
                break

            data = response.json()['response']['award']
            
            if len(data) < ROWS_PER_PAGE:
                all_results.extend(data)
                break
            
            all_results.extend(data)
            offset += ROWS_PER_PAGE
        
        except requests.exceptions.JSONDecodeError as e:
            print("Error:", e)
            print("Response Preview:", response.text[:250])
            break
        
    return all_results

METADATA = {
    'name': 'nsf.gov',
    'raw_path': RAW_DATA_PATH,
    'fetch_fn': fetch_data,
    'transform_fn': '',
    'search_terms': SEARCH_TERMS
}

