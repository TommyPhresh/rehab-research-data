import requests, hashlib, itertools
from datetime import datetime
from bs4 import BeautifulSoup

def generate_id(text):
    return hashlib.md5(text.strip().lower().encode()).hexdigest()[:12]

def parse_weird_date(date_str):
    clean_date = date_str.replace(".", " ").strip()
    month, rest = clean_date[:clean_date.find(" ")], clean_date[clean_date.find(" "):]
    real_month = ""
    match month:
        case "Jan":
            real_month = "Jan"
        case "Feb":
            real_month = "Feb"
        case "March":
            real_month = "Mar"
        case "April":
            real_month = "Apr"
        case "May":
            real_month = "May"
        case "June":
            real_month = "Jun"
        case "July":
            real_month = "Jul"
        case "Aug":
            real_month = "Aug"
        case "Sept":
            real_month = "Sep"
        case "Oct":
            real_month = "Oct"
        case "Nov":
            real_month = "Nov"
        case "Dec":
            real_month = "Dec"
    clean_datetime = datetime.strptime(real_month + rest, "%b %-d, %Y")
    return clean_datetime.strftime("%Y-%m-%d")

def scrape_pcori_page(num):
    url = f"https://www.pcori.org/funding-opportunities?page={num}"
    headers ={
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
    container = soup.find('div', class_='view__content')
    if not container:
        return []
    table = container.find('table', class_='cols-3')
    if not table:
        return []
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        info_bundle = cols[0]
        title_tag = info_bundle.find('a')
        name = title_tag.get_text(strip=True)
        link = "https://www.pcori.org" + title_tag['href'] if title_tag['href'].startswith('/') else title_tag['href']
        desc = "Patient-Centered Outcomes Research Grant"
        deadline = parse_weird_date(cols[2].get_text(strip=True))
        results.append({
            "id": generate_id(link + name),
            "name": name,
            "org": "PCORI",
            "desc": desc,
            "deadline": deadline,
            "link": link,
            "isGrant": 1,
        })
    return results

def scrape_pcori():
    results = []
    i = 1
    page_results = scrape_pcori_page(0)
    results.append(page_results)
    while len(page_results) > 0:
        page_results = scrape_pcori_page(i)
        results.append(page_results)
        i += 1
    return list(itertools.chain(*results))
