import hashlib, pandas as pd

def generate_id(link):
    return hashlib.md5(link.strip().lower().encode()).hexdigest()[:12]

def scrape_neilsen():
    raw_data = [
        {
            "name": "Spinal Cord Injury Research on the Translational Spectrum - Translational Spectrum Grants",
            "link": "https://chnfoundation.org/programs/spinal-cord-injury-research-on-the-translational-spectrum-2/",
            "desc": "Supporting the wide array of research opportunities to identify effective treatments and move them from the laboratory to clinical testing, the SCIRTS portfolio encourages limitless creativity and leadership in research. Two-to-three-year grants supporting research that addresses functional outcomes and complications after SCI, across the acute and chronic injury periods. Studies should demonstrate novelty, scientific merit, and the potential for substantial impact on treatment and care, with meaningful inclusion of individuals with lived SCI experience is encouraged.",
            "deadline": '2027-05-22',
        },
        {
            "name": "Spinal Cord Injury Research on the Translational Spectrum - Postdoctoral Fellowships",
            "link": "https://chnfoundation.org/programs/spinal-cord-injury-research-on-the-translational-spectrum-2/",
            "desc": "Supporting the wide array of research opportunities to identify effective treatments and move them from the laboratory to clinical testing, the SCIRTS portfolio encourages limitless creativity and leadership in research. Two-year support of postdoctoral training to prepare for independent SCI research careers. Fellows receive mentorship from experienced SCI investigators, with a focus on scientific development, career advancement, and conducting research that aligns with the Neilsen Foundation's mission.",
            "deadline": '2027-05-22',
        },
        {
            "name": "Creating Opportunity & Independence - Community Support Grants",
            "link": "https://chnfoundation.org/programs/creating-opportunity-independence/",
            "desc": "The Creating Opportunity & Independence (CO&I) portfolio supports nonprofit partners that provide programs and services to empower people with spinal cord injury (SCI) to achieve active, fulfilling lives. This one-year or two-year funding helps nonprofit organizations improve the lives of people with SCI by supporting: Community Activities - where people are actively engaged and interact with peers; Life Transitions - for organizations that assist in finding practical solutions after injury and promote successful integration into homes, workplaces, and communities; Accessibility For All - projects that remove barriers that prevent full participation in society.",
            "deadline": '2027-01-25',
        },
        {
            "name": "Psychosocial Research - Postdoctoral Fellowships",
            "link": "https://chnfoundation.org/programs/psychosocial-research/",
            "desc": "The Psychosocial Research (PSR) portfolio supports the study of people's psychological and social wellbeing and research to develop and test interventions that improve an individual's mental, behavioral, and social welfare following spinal cord injury (SCI). The goal is to build and disseminate solutions that individuals, caregivers, clinicians, and communities can incorporate to address emotional wellbeing and barriers to social engagement. The portfolio seeks to advance meaningful participation of people with lived experience in SCI research design and execution. Two-year Postdoctoral Fellowships encourage early-career mentored training to build interest in the field and to encourage researchers from related health disciplines to undertake training in psychosocial research focused on spinal cord injury.",
            "deadline": '2027-03-04',
        },
        {
            "name": "Psychosocial Research - Investigational Grants",
            "link": "https://chnfoundation.org/programs/psychosocial-research/",
            "desc": "The Psychosocial Research (PSR) portfolio supports the study of people's psychological and social wellbeing and research to develop and test interventions that improve an individual's mental, behavioral, and social welfare following spinal cord injury (SCI). The goal is to build and disseminate solutions that individuals, caregivers, clinicians, and communities can incorporate to address emotional wellbeing and barriers to social engagement. The portfolio seeks to advance meaningful participation of people with lived experience in SCI research design and execution. Two-year funding that supports research to improve understanding of psychosocial issues and provide insights needed to develop approaches that improve the lives of people affected by spinal cord injury. Studies in this category may involve the development and early testing of an intervention, although this is not a requirement.",
            "deadline": '2027-03-04',
        },
        {
            "name": "Psychosocial Research - Interventional Testing Grants",
            "link": "https://chnfoundation.org/programs/psychosocial-research/",
            "desc": "The Psychosocial Research (PSR) portfolio supports the study of people's psychological and social wellbeing and research to develop and test interventions that improve an individual's mental, behavioral, and social welfare following spinal cord injury (SCI). The goal is to build and disseminate solutions that individuals, caregivers, clinicians, and communities can incorporate to address emotional wellbeing and barriers to social engagement. The portfolio seeks to advance meaningful participation of people with lived experience in SCI research design and execution. Funding for up to three years to support work that leads to the creation, adaptation, and/or refinement of an intervention to address psychosocial challenges for those affected by spinal cord injury. Studies in this category include testing the feasibility, acceptability, and/or initial efficacy of the developed intervention.",
            "deadline": '2027-03-04',
        },
    ]
    results = []
    for item in raw_data:
        results.append({
            "id": generate_id(item['link'] + item['name']),
            "name": item['name'],
            "org": "Craig H. Neilsen Foundation",
            "desc": item['desc'],
            "deadline": item['deadline'],
            "link": item['link'],
            "isGrant": 1,
        })
    return pd.DataFrame(results)