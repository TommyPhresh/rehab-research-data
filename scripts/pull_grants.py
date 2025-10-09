'''
This file efficiently handles incremental pulls from grants.gov.
Uses a constant list of terms to pull only relevant and new/updated data.
'''
import sys, os
# The path to packages on the C: drive
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if c_path not in sys.path:
    sys.path.append(c_path)

import requests, json
from datetime import datetime

API_URL = "https://api.grants.gov/v1/api/search2"
SEARCH_TERMS = [
    "Interventional Spine", "Pain Management", "Electromyography", "Electrodiagnostics", "Radiculopathy",
    "Musculoskeletal Rehabilitation", "Ultrasound", "Pediatric Rehabilitation", "Neuropsychology",
    "Rehabilitation Psychology", "Traumatic Brain Injury", "Stroke Rehabilitation", "Spasticity",
    "Physical Therapy", "Occupational Therapy", "Rehabilitation", "Limb Loss",
]
ROWS_PER_PAGE = 100
RAW_DATA_PATH = "data/raw/grants.jsonl"

'''
Returns results across all search terms
Params:
(list[str], str) -> list[dict]
* `terms: list[str]`. List of all search terms desired for grants.gov.
* `last_refresh: str`. YYYY-MM-DD format string representing last successful pull.
'''
def fetch_data(terms, last_refresh):
    # convert last_refresh to datetime for filtering later
    try:
        last_refresh_datetime = datetime.strptime(last_refresh, "%Y-%m-%d").date()
    except ValueError:
        last_refresh_datetime = datetime(1900,1,1).date()
        
    # main loop: search through all pages for all search terms
    all_results = []
    query = " OR ".join(terms)
    start_record = 0
    while True:
        params = {
            "keyword": query,
            "oppStatuses": "forecasted|posted",
            "rows": ROWS_PER_PAGE,
            "startRecordNum": start_record
        }
        try:
            response = requests.post(API_URL, json=params)
            response.raise_for_status()
            current_page = response.json().get('data', {}).get('oppHits', [])
            curr = sorted(current_page,
                          key=lambda item: datetime.strptime(item['openDate'], "%m/%d/%Y").date(),
                          reverse=True)
            oldhead = False
            for grant in curr:
                print(f"Finished page {start_record // ROWS_PER_PAGE}. oldhead: {oldhead}")
                date_string = grant.get('openDate')
                if date_string:
                    try:
                        open_date = datetime.strptime(grant['openDate'], "%m/%d/%Y").date()
                        if open_date <= last_refresh_datetime:
                            oldhead = True
                            break
                    except ValueError:
                        pass
                all_results.append(grant)
            if oldhead:
                break
            start_record += ROWS_PER_PAGE
        except requests.exceptions.RequestException as e:
            print(f"Error:", e)
            break
    return all_results
                

'''
Transforms data from grants.gov format to rehab-research.com format.
'''
def transform_data(raw_data):
    transformed_data = []
    for grant in raw_data:
        close_date_string = grant.get('closeDate')
        try:
            close_date = datetime.strptime(close_date_string, "%m/%d/%Y").date().strftime("%Y-%m-%d")
        except ValueError: 
            close_date = "This grant is forecasted; no close date posted yet."
        if isinstance(grant['id'], str):
            url = f"https://www.grants.gov/search-results-detail/{grant['id']}"
        else:
            url = ''
        transformed_data.append({
            'name': grant['title'],
            'org': grant['agency'],
            'desc': "Please click link to view description",
            'deadline': close_date,
            'link': url,
            'isGrant': True
        })
    return transformed_data
                
METADATA = {
    "name": API_URL,
    "raw_path": RAW_DATA_PATH,
    "fetch_fn": fetch_data,
    "transform_fn": transform_data,
    "search_terms": SEARCH_TERMS
}
