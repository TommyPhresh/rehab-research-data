from datetime import datetime 

def fetch(opt=[], opt=''): return []

def tomberg(opt=[]):
    link = "https://www.tombergphilanthropies.org/about-our-grants"
    now = datetime.now()
    if (now.month <= 7) and (now.day <= 7):
        due_date = datetime(now.year, 7, 21)
    else:
        due_date = datetime(now.year + 1, 7, 21)
    return [{
        'name': 'Tomberg Family Philanthropies',
        'org': 'Tomberg & Brecher Charitable Funds',
        'desc': 'The Tomberg Family Philanthropies only makes grants to 501(c)(3) nonprofit organizations based in the United States and certain government entities or public institutions in the United States such as public schools and universities. We fund projects worldwide that are run by these organizations. Our grants normally range from $5,000 to $20,000.',
        'deadline': due_date.strftime("%Y-%m-%d"),
        'link': link, 'isGrant': True
    }]

METADATA = {
    'name': 'Tomberg Family Philanthropies',
    'raw_path': "D:\\Personal\\rehab-research-data\\data",
    'fetch_fn': fetch,
    'transform_fn': tomberg,
    'search_terms': []
    }