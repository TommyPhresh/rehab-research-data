from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import pandas as pd

link = "https://professional.heart.org/en/research-programs/aha-funding-opportunities"
prefix = 'https://professional.heart.org'

'''
fetch_aha pulls raw HTML for grants from the AHA website.
'''
def fetch_aha():
    driver = webdriver.Chrome()
    driver.get(link)
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((
        By.CLASS_NAME, 'phd-shadow-box'
    )))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    categories = soup.find_all('div', class_='phd-shadow-box')
    data = []
    for category in categories:
        try:
            rows = category.find('table', class_='table table-striped').find('tbody').find_all('tr')
        except Exception as e:
            print('NONFATAL', e)
            continue
        for row in rows:
            data.append(row)
    return data

'''
transform_aha converts raw HTML AHA grants to rehab-research.com format
'''
def transform_aha(html):
    transformed_data = []
    for row in html:
        try:
            transformed_data.append({
                'name': row.find('a').text.strip(),
                'org': 'American Heart Association',
                'desc': row.text.split('\n')[-1].strip(),
                'deadline': row.text.split('\n')[1].strip(),
                'link': prefix + row.find('a')['href'],
                'isGrant': True,
            })
        except Exception as e:
            print('TRANSFORMATION ERROR', e)
            continue
    return transformed_data


METADATA = {
    "name": "American Heart Association",
    "raw_path": RAW_DATA_PATH,
    "fetch_fn": fetch_aha,
    "transform_fn": transform_aha,
}
