import requests, hashlib
from bs4 import BeautifulSoup

def generate_id(text):
    return hashlib.md5(text.strip().lower().encode())[:12]

def scrape_nidilrr():
    url = "https://acl.gov/grants/open-opportunities"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    rows = soup.find_all('div', class_='views-row')
    for row in rows:
        name = row.find('h2').get_text(strip=True)
        is_nidilrr = any(x in name for x in ['nidilrr','90re','90if','90si','90ar'])
        if not is_nidilrr:
            continue
        link = row.find('a', href=True)['href']
        desc = "ACL was created around the fundamental principle that all people, regardless of their age or disability, should be able to live independently and participate fully in their communities."
        deadline = '9999-12-31'
        results.append({
            "id": generate_id(link + name),
            "name": name,
            "org": "NIDILRR",
            "desc": desc,
            "deadline": deadline,
            "link": link,
            "isGrant": 1,
        })
    return results
