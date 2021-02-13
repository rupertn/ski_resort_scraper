import requests
from bs4 import BeautifulSoup as bs
import time

base_url = 'https://www.skicentral.com/'

region_list = ['britishcolumbia', 'alberta', 'montana', 'idaho', 'wyoming', 'utah', 'colorado', 'california', 'nevada',
               'oregon', 'washington', 'arizona', 'newmexico', 'alaska']


def get_resort_urls(reg):
    full_url = base_url + reg + '.html'
    page = requests.get(full_url)
    soup = bs(page.text, 'html.parser')

    for resort in soup.find_all('div', class_='resorttitle'):
        link = resort.find('a')
        resort_urls.append(base_url + link['href'])


resort_urls = []
for region in region_list:
    time.sleep(1)
    get_resort_urls(region)

print(resort_urls)
