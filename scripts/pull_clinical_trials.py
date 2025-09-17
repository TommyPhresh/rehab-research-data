# This file efficiently handles incremental pulls from clinicaltrials.gov
# Uses a constant list of terms to pull only relevant and updated/new data.

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

'''
Updates the timestamp of last successful refresh
() -> ()
'''
def update_last_refresh():
    with open(LAST_PULL_DATE_FILE, 'r') as file:
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
        "filter.lastRefreshPostDate": f"GE{last_refresh"
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
