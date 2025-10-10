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

import requests, json
from datetime import datetime


API_URL = "https://clinicaltrials.gov/api/v2/studies"
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

'''
Returns results across all search terms
(dict[list[str]], str) -> list[dict]
Params:
* `search_terms_obj`: Search terms dictionary with one entry for conditions list and one for interventions list.
* `last_refresh`: YYYY-MM-DD date representing last ping to API.
Return
* List of JSON document. Each JSON document is a study.
'''
def fetch_data(search_terms_obj, last_refresh):
    params = {
        "format": "json",
        "query.locn": "United States",
        "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|ACTIVE_NOT_RECRUITING|ENROLLING_BY_INVITATION",
        "pageSize": PAGE_SIZE,
        "sort": "LastUpdatePostDate"
    }

    all_results = []
    last_refresh_datetime = datetime.strptime(last_refresh, "%Y-%m-%d").date()
    for search_type in search_terms_obj:
        for term in search_terms_obj[search_type]:
            if search_type == "conditions":
                params["query.cond"] = term
            else:
                params["query.intr"] = term
            page_token = None

            while True:
                if page_token:
                    params['pageToken'] = page_token
                print(f"Searching for {term}...")
                response = requests.get(API_URL, params=params)

                if response.status_code != 200:
                    print(f"Error: {response.text}")
                    break

                try: 
                    data = response.json()
                    page_results = data.get("studies", [])
                    if not page_results:
                        break
                    oldhead = False
                    for opp in page_results:
                        date_string = opp['protocolSection']['statusModule']['lastUpdatePostDateStruct']['date']
                        if date_string:
                            try:
                                post_date = datetime.strptime(date_string, "%Y-%m-%d").date()
                                if post_date <= last_refresh_datetime:
                                    oldhead = True
                                    break
                            except ValueError:
                                pass
                        all_results.append(opp)
                    if oldhead:
                        break
                    page_token = data.get("nextPageToken")
                    if not page_token:
                        break
                except requests.exceptions.JSONDecodeError as e:
                    print("Error:", e)
                    print("RESPONSE PREVIEW:", response.text[:250])
                    break
    return all_results

'''
Transforms into universal format.
'''
def transform_data(raw_data):
    transformed_data = []
    for study in raw_data:
        protocol = study.get('protocolSection', {})
        identification = protocol.get('identificationModule', {})
        description = protocol.get('descriptionModule', {})
        status = protocol.get('statusModule', {})
        sponsor = protocol.get('sponsorCollaboratorsModule', {})

        nct_id = identification.get('nctId')

        # Priority Order: Sponsor, Organization, default
        org = None
        org = sponsor.get('leadSponsor', {}).get('name')
        if not org:
            org = identification.get('organization', {}).get('fullName')
        org = org if org else 'No organization listed'

        # Priority Order: Primary completion, completion, default
        deadline = None
        deadline = status.get('primaryCompletionDateStruct', {}).get('date')
        if not deadline:
            deadline = status.get('completionDateStruct', {}).get('date')
        deadline = deadline if deadline else '9999-12-31'

        link = f'https://clinicaltrials.gov/study/{nct_id}' if nct_id else ''
        transformed_data.append({
            'name': identification.get('briefTitle', 'No name given'),
            'org': org,
            'desc': description.get('briefSummary', 'No description given'),
            'deadline': deadline,
            'link': link,
            'isGrant': False
            })
    return transformed_data

METADATA = {
    'name': 'clinicaltrials.gov',
    'raw_path': RAW_DATA_PATH,
    'fetch_fn': fetch_data,
    'transform_fn': transform_data,
    'search_terms': SEARCH_TERMS
    }

