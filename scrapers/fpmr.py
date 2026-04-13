import hashlib, pandas as pd

def generate_id(link):
    return hashlib.md5(link.strip().lower().encode()).hexdigest()[:12]

def scrape_fpmr():
    raw_data = [
        {
            "name": "Richard Materson ERF New Investigator Research Grants",
            "link": "https://foundationforpmr.org/research-grants/richard-materson-erf-new-investigator-research-grants/",
            "desc": "Three grants of $10,000 each for young investigators 5 years or less out of training.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Gabriella Molnar Pediatric PM&R Research Grant",
            "link": "https://foundationforpmr.org/research-grants/gabriella-molnar-pediatric-pmr-research-grant/",
            "desc": "One grant of $10,000 for research on a topic related to pediatric rehabilitation.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Encompass Health Midcareer Investigator Research Grant",
            "link": "https://foundationforpmr.org/research-grants/encompass-midcareer-investigator-research-grant/",
            "desc": "One grant of $25,000 to a proven physiatric investigator to expand his/her research in a new direction. Supported by a grant from Encompass.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Tactile Medical Cancer Rehabilitation Research Grant",
            "link": "https://foundationforpmr.org/research-grants/tactile-medical-cancer-rehabilitation-research-grant/",
            "desc": "One grant of $10,000 for research on a topic related to physiatric rehabilitation for individuals with cancer-related disability. Supported by a grant from Tactile Medical.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Scott Nadler PASSOR Musculoskeletal Research Grant",
            "link": "https://foundationforpmr.org/research-grants/scott-nadler-passor-musculoskeletal-research-grant/",
            "desc": "One grant of $30,000 for research on a topic related to musculoskeletal rehabilitation",
            "deadline": '2027-05-01',
        },
        {
            "name": "Martin Grabois Chronic Pain Rehabilitation Research Grant",
            "link": "https://foundationforpmr.org/research-grants/",
            "desc": "One grant of $10,000 for physiatric research focused on the physiology of chronic pain and its clinical management.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Richard Herman Neurologic Rehabilitation Research Grant",
            "link": "https://foundationforpmr.org/research-grants/",
            "desc": "One grant of $10,000 focused on physiatric research in neuroscience, neurophysiology, or rehabilitation neuroengineering.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Dorothea Glass PM&R Lifestyle Research Grant",
            "link": "https://foundationforpmr.org/research-grants/",
            "desc": "One grant of $10,000 for physiatric research focused on sexuality, relationship, and lifestyle issues affecting individuals with disability.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Nobis Rehabilitation Partners Inpatient Rehabilitation Research Grant",
            "link": "https://foundationforpmr.org/research-grants/",
            "desc": "One grant of $30,000 for physiatric research focused on best practices, comparative effectiveness, transition of care or other inpatient-specific rehabilitation topics.",
            "deadline": '2027-05-01',
        },
        {
            "name": "Justus Lehmann Research Grant",
            "link": "https://foundationforpmr.org/research-grants/",
            "desc": "Due to a lack of funding, the Justus Lehmann biomechanics research grant is not available this year.",
            "deadline": '2027-05-01',
        }
    ]
    results = []
    for item in raw_data:
        results.append({
            "id": generate_id(item['link'] + item['name']),
            "name": item['name'],
            "org": "Foundation for PM&R",
            "desc": item['desc'],
            "deadline": item['deadline'],
            "link": item['link'],
            "isGrant": 1,
        })
    return pd.DataFrame(results)