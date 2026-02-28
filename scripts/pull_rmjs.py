from datetime import datetime 

def fetch(opt=[], opt=''): return []

def rmjsf(opt=[]):
    link = "https://www.rmjsfoundation.org/giving"
    now = datetime.now()
    if (now.month < 9):
        due_date = datetime(now.year, 9, 1)
    else:
        due_date = datetime(now.year + 1, 9, 1)
    return [{
        'name': 'Robert & Mary Jane Smith Foundation Grant',
        'org': 'Robert & Mary Jane Smith Foundation',
        'desc': 'Founded in 2017, the Robert and Mary Jane Smith Foundation is dedicated to supporting nonprofit institutions based in the United States. Our foundation prioritizes support for the development and education of young people, medical institutions and research, cultural and faith-based organizations, and humanitarian efforts.',
        'deadline': due_date.strftime("%Y-%m-%d"),
        'link': link, 'isGrant': True
    }]

METADATA = {
    'name': 'Robert & Mary Jane Smith Foundation',
    'raw_path': "D:\\Personal\\rehab-research-data\\data",
    'fetch_fn': fetch,
    'transform_fn': rmjsf,
    'search_terms': []
    }