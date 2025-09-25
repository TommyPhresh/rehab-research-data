'''
This file efficiently handles incremental pulls from clinicaltrials.gov
Uses a constant list of terms to pull only relevant and updated/new data.
'''

import sys, os
# The path to packages on the C: drive
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if c_path not in sys.path:
    sys.path.append(c_path)

import requests, json, pandas as pd
from datetime import datetime

API_URL = "https://clinicaltrials.gov/v2/studies"
SEARCH_TERMS = {
    "conditions": [
        "Limb Loss", "Arthritis", "Osteoarthritis", "Herniated Disc", "Scoliosis", "Spinal Stenosis",
    "Traumatic Brain Injury", "Stroke", "Balance Disorder", "Parkinson's Disease",
    "Spinal Cord Injury", "Brain Tumor", "Spine Tumor", "Multiple Sclerosis",
    "Pelvic Floor Disorder", "Concussion", "Developmental Disability", "Ataxia",
    "Functional Neurologic Disorder", "Heart Failure", "Heart Attack", "Angioplasty",
    "Aortic Aneurysm", "Aortic Dissection", "Angina", "Aortic Stenosis", "Arrythmia",
    "Atrial Fibrillation", "Bradycardia", "Cardiomyopathy", "Carotid Artery Disease",
    "Coronary Artery Disease", "Heart Valve Disease", "Hypertrophic Cardiomyopathy",
    "Adult Congenital Heart Disease", "Alzheimer's Disease", "Dementia", "Hand Pain",
    "Wrist Pain", "Lymphedema", "Major Multiple Trauma", "Cerebral Palsy",
    "Guillain-Barre Syndrome", "Amyotrophic Lateral Sclerosis", "Cancer", "Spasticity",
    "Chronic Obstructive Pulmonary Disease", "Coronavirus", "Bronchiectasis",
    "Nontuberculous Mycobacteria", "Speech Disorder", "Swallowing Disorder",
    "Dysphagia", "Dysarthria", "Neurodegenerative Speech Disorder", "Aphasia",
    "Tendonitis", "High Cholesterol", "Sickle Cell Disease", "Facial Paralysis",
    "Trigeminal Neuralgia", "Left Atrial Appendage Occlusion", "Radiculopathy"
        ],
    "interventions": [
        "Lower Extremity Reconstruction", "Limb-Saving Care", "Joint Replacement Surgery",
    "Hip Replacement", "Knee Replacement", "Shoulder Replacement", "Elbow Replacement",
    "Neurological Rehabilitation", "Neurosurgery", "Neuromedicine Pain Management",
    "Neuroradiology", "Vestibular Testing", "Acute Rehabilitation", "Vestibular Rehabilitation",
    "Neurorehabilitation", "Spinal Cord Injury Rehabilitation", "Cardiac Rehabilitation", "Stenting",
    "Coronary Artery Bypass Grafting", "Heart Valve Repair", "Heart Valve Replacement",
    "Minimally Invasive Cardiac Surgery", "Minimally Invasive Valve Surgery",
    "Open Heart Surgery", "Transcatheter Aortic Valve Replacement","Ventricular Assist Device",
    "Heart Transplant", "Cardiac Surgery", "Cognitive Rehabilitation", "Electrodiagnostic Study",
    "Hand Rehabilitation", "Wrist Rehabilitation", "Plastic Surgery", "Reconstructive Surgery",
    "Performing Arts Medicine", "Medically Complex Rehabilitation", "Inpatient Acute Rehabilitation",
    "Physical Therapy", "Occupational Therapy", "Vascular Care", "Cancer Rehabilitation",
    "Pediatric Rehabilitation", "Prosthesis", "Pulmonary Rehabilitation", "Neuromodulation",
    "Botox Therapy", "Speech Therapy", "Sports Injury Rehabilitation", "Aquatic Therapy",
    "Sport Psychology", "Balance Training", "Neuropsychology", "Palliative Care",
    "Spinal Injection"
        ]
    }
PAGE_SIZE = 1000
RAW_DATA_PATH = "data/raw/clinical_trials.jsonl"
LAST_PULL_DATE_FILE = "data/last_pull_date.txt"

'''
Loads the timestamp of last successful refresh
() -> ()
'''
def get_last_refresh():
    try:
        with open(LAST_PULL_DATE_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "1900-01-01"
    except Exception as e:
        print(f"Error: {e}")
        return "1900-01-01"

'''
Updates the timestamp of last successful refresh
() -> ()
'''
def update_last_refresh():
    with open(LAST_PULL_DATE_FILE, 'w') as file:
        file.write(datetime.now().strftime("%Y-%m-%d"))

'''
Returns results for one search term
(str, str, str) -> list[dict]
Params:
* `search_type`: Either "conditions" or "interventions". Controls what type of results are returned.
* `term`: Search term. 
* `last_refresh`: YYYY-MM-DD date representing last ping to API.
Return
* List of JSON document. Each JSON document is a study.
'''
def fetch_data(search_type, term, last_refresh):
    params = {
        "format": "json",
        "query.locs": "United States",
        "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|ACTIVE_NOT_RECRUITING|ENROLLING_BY_INVITATION",
        "pageSize": PAGE_SIZE,
        "filter.lastRefreshPostDate": f"{last_refresh}"
        }
    if search_type == "conditions":
        params["query.cond"] = term
    else:
        params["query.intr"] = term

    all_results = []
    page_token = None

    while True:
        if page_token:
            params['pageToken'] = page_token
        print(f"Searching for {term}...")
        response = requests.get(API_URL, params=params)

        if response.status_code != 200:
            print(f"Error: {response.text}")
            break

        data = response.json()
        results = data.get("studies", [])
        all_results.extend(results)
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return all_results

'''
Appends new search results to JSONL file (raw data) defined for clinicaltrials.
list[dict] -> ()
Params:
* `results`: List of JSON documents, each JSON document is a study
'''
def save_raw_data(results):
    with open(RAW_DATA_PATH, 'w') as file:
        for study in results:
            json.dump(study, file)
            file.write('\n')
    print(f"Saved {len(results)} new studies.")

'''
Appends results of searches for each term in SEARCH_TERMS in one list.
Dumps results list into raw data JSONL file.
() -> ()
'''
def main():
    last_refresh = get_last_refresh()
    all_results = []
    print("Beginning searches...")
    for term in SEARCH_TERMS["conditions"]:
        results = fetch_data("conditions", term, last_refresh)
        all_results.extend(results)
    print("Finished searching conditions...")
    
    for term in SEARCH_TERMS["interventions"]:
        results = fetch_data("interventions", term, last_refresh)
        all_results.extend(results)

    print("Finished searching interventions...")
    print(f"All searches returned {len(all_results)} total results.")
    if all_results:
        save_raw_data(all_results)
        update_last_refresh()

    else:
        print("No new studies found since last refresh.")

if __name__ == "__main__":
    main()
        
