import requests
from bs4 import BeautifulSoup as bs
import time


def get_resort_urls(reg, base_url='https://www.skicentral.com/'):
    full_url = base_url + reg + '.html'
    page = requests.get(full_url)
    soup = bs(page.text, 'html.parser')

    resort_urls = []

    for resort in soup.find_all('div', class_='resorttitle'):
        link = resort.find('a')
        resort_urls.append(base_url + link['href'])

    return resort_urls


def get_resort_info(mountain_url):
    page = requests.get(mountain_url)
    soup = bs(page.text, 'html.parser')

    info = []


region_list = ['britishcolumbia', 'alberta', 'montana', 'idaho', 'wyoming', 'utah', 'colorado', 'california', 'nevada',
               'oregon', 'washington', 'arizona', 'newmexico', 'alaska']

start = time.now()
for region in region_list:
    mountain_urls = get_resort_urls(region)

    for url in mountain_urls:
        get_resort_info(url)
