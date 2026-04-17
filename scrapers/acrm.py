import hashlib, pandas as pd

def generate_id(text):
    return hashlib.md5(text.strip().lower().encode())[:12]

def scrape_acrm():
    raw_data = [
        {
            "name": "Joshua B. Cantor Award",
            "link": "https://acrm.org/brain-injury-awards",
            "desc": "The Cantor Scholar Award is presented by the Brain Injury Interdisciplinary Special Interest Group (BI-ISIG) to a BI-ISIG member in recognition of outstanding research that is judged to be a significant contribution to the field of brain injury rehabilitation. This memorial award is named in honor of Dr. Joshua B. Cantor, who was an ACRM and BI-ISIG member well-known for his research on life after TBI.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Excellence in Cancer Rehabilitation Award",
            "link": "https://acrm.org/cancer-rehabilitation-awards",
            "desc": "The Excellence in Cancer Rehabilitation Award recognizes someone who has demonstrated excellence in the field of interdisciplinary cancer rehabilitation in one or more important areas including, but not limited to, clinical care, medical education or research.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Distinguished Guest Lecturer in Cancer Rehabilitation & Survivorship Care Award",
            "link": "https://acrm.org/cancer-rehabilitation-awards",
            "desc": "The Distinguished Guest Lecturer in Cancer Rehabilitation & Survivorship Care Award recognizes those making important contributions to the advancement of oncology care.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Career Development Outstanding Mentor Award",
            "link": "https://www.acrm.org/cdng-awards",
            "desc": "The Career Development Outstanding Mentor Award was established in 2016 to honor those who have significantly contributed through mentorship to the development of early career rehabilitation professionals, the Early Career Development Course and the Career Development Networking Group's Mentoring Task Force.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Excellence in CIRM Research Award",
            "link": "https://www.acrm.org/cirm-awards",
            "desc": "The Excellence in Complementary & Integrative Rehabilitation Medicine Research Award recognizes an outstanding researcher who has demonstrated scientific excellence regarding the use and integration of complementary, holistic and integrative health approaches related to important rehabilitation medicine areas including healthcare, education and policy.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Women in Neurodegenerative Disease Rehabilitation Science Award",
            "link": "https://www.acrm.org/ndng-awards",
            "desc": "This award is given by the ACRM Neurodegenerative Diseases Networking Group (NDNG) to acknowledge world-class rehabilitation research conducted by a female scientist in the rehabilitation research field of multiple sclerosis, amyotrophic lateral sclerosis, Parkinson's, dementia, Alzheimer's or related neurodegenerative disease.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Pediatric Rehabilitation Award Lecture",
            "link": "https://www.acrm.org/pediatric-awards",
            "desc": "The Pediatric Rehabilitation Award Lecture was created in 2016 to recognize the Pediatric Rehabilitation professional who has made outstanding contribution to the field.",
            "deadline": '2027-03-01',
        },
        {
            "name": "SCI-ISIG Margaret Nosek Award",
            "link": "https://acrm.org/spinal-cord-injury-awards",
            "desc": "The SCI-ISIG Margaret Nosek Award recognizes an individual who demonstrates drive and commitment to advancing scientific knowledge, developing standards of clinical practice, raising awareness, and advocating for appropriate health care and community support for women with disabilities. Dr. Margaret Nosek was an internationally recognized authority on the health of women with disabilities and the Margaret Nosek Award recognizes her contributions through more than 30 years of sharing/disseminating knowledge as a researcher and advocate of disability rights.",
            "deadline": '2027-03-01',
        },
        {
            "name": "ACRM Young Investigator Award in Post-Acute Stroke Rehabilitation",
            "link": "https://acrm.org/stroke-awards",
            "desc": "The award is given to acknowledge world-class rehabilitation research conducted by a female scientist in the rehabilitation research field of Multiple Sclerosis, Amyotrophic Lateral Sclerosis, Parkinson's, dementia, Alzheimer's disease or related neurodegenerative disease.",
            "deadline": '2027-03-01',
        },
        {
            "name": "ACRM Award for Excellence in Post-Acute Stroke Rehabilitation",
            "link": "https://acrm.org/stroke-awards",
            "desc": "ACRM is dedicated to advancing post-acute care, advocacy, and scientific efforts for survivors of stroke and their families. This award recognizes a clinician or researcher (individual or group) (e.g., a care team, a research team, a clinical group) who has advanced the field through their scientific and/or clinical efforts in the area of post-acute stroke.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Gold Key Award",
            "link": "https://www.acrm.org/gold-key-award",
            "desc": "This award was established in 1932 as a certificate of merit for members of the medical and allied professions who had rendered extraordinary service to the cause of rehabilitation.",
            "deadline": '2027-03-01',
        },
        {
            "name": "John Stanley Coulter Award",
            "link": "https://www.acrm.org/john-stanley-coulter-award",
            "desc": "The Coulter Lecture honors leaders whose contributions reflect the legacy of Dr. John Stanley Coulter. Established after his passing in 1949, the lecture has been a signature part of every ACRM Annual Meeting since 1951. Dr. Coulter - widely regarded as a pioneer of physical medicine and rehabilitation - served in World War I, advanced early PT and OT practices, published extensively, and helped establish key national standards for PM&R.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Distinguished Member Award",
            "link": "https://www.acrm.org/distinguished-member-award",
            "desc": "Established in 1988, the Distinguished Member Award honors an ACRM member who significantly contributes to the development and functioning of ACRM. Qualified nominees are ACRM members who provide extraordinary service as a member or chair of a committee, task force, ISIG, or networking group.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Mitchell Rosenthal Mid-Career Award",
            "link": "https://www.acrm.org/mitchell-rosenthal-midcareer-award",
            "desc": "The Mitchell Rosenthal Mid-Career Award was established in 2013 to recognize clinician-scientists working in the spirit of Dr. Rosenthal in the field of brain injury rehabilitation.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Deborah L. Wilkerson Early Career Award",
            "link": "https://www.acrm.org/deborah-l-wilkerson-early-career-award",
            "desc": "This award is given in memory of Deborah L. Wilkerson, former ACRM president and fellow. Deborah was devoted to improving the quality of rehabilitation and independent living services. She demonstrated a commitment to person-centered services and served as a powerful advocate for individuals with disabilities.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Edward Lowman Award",
            "link": "https://www.acrm.org/edward-lowman-award",
            "desc": "The Lowman Award was established in 1989 in honor of Edward Lowman, MD, who recognized the importance of multidisciplinary teams in rehabilitation.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Elizabeth and Sidney Licht Award",
            "link": "https://www.acrm.org/elizabeth-and-sidney-licht-award",
            "desc": "This award honors Sidney Licht, MD, a longtime ACRM member and former president, and his wife Elizabeth, who was the publisher of the Physical Medicine Library. The Elizabeth and Sidney Licht Award recognizes excellence in scientific writing in rehabilitation medicine.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Women in Rehabilitation Science",
            "link": "https://www.acrm.org/women-in-rehabilitation-science-award",
            "desc": "The ACRM Women in Rehabilitation Science Award is given in recognition of world-class rehabilitation research conducted by a female scientist.",
            "deadline": '2027-03-01',
        },
        {
            "name": "Excellence in Health Equity Research Award",
            "link": "https://www.acrm.org/excellence-in-health-equity-research-award",
            "desc": "This award recognizes the scientific contributions of researchers that promote health equity or address disparities in rehabilitation medicine.",
            "deadline": '2027-03-01',
        },
    ]
    results = []
    for item in raw_data:
        results.append({
            "id": generate_id(item['link'] + item['name']),
            "name": item['name'],
            "org": "American Congress of Rehabilitation Medicine",
            "desc": item['desc'],
            "deadline": item['deadline'],
            "link": item['link'],
            "isGrant": 0,
        })
    return results
