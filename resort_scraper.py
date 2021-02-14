import requests
from bs4 import BeautifulSoup as bs
import time


def get_resort_urls(reg):
    base_url = 'https://www.skicentral.com/'
    full_url = base_url + reg + '.html'

    page = requests.get(full_url)
    soup = bs(page.text, 'html.parser')

    resort_urls = []

    for resort in soup.find_all('div', class_='resorttitle'):
        link = resort.find('a')
        resort_urls.append(base_url + link['href'])

    return resort_urls


def get_overview_stats(info, soup):
    overview_table = soup.find('table', id='mountainstatistics').find('tbody')  # main mountain stats
    for row in overview_table.find_all('tr')[:8]:
        info.append(row.find_all('td')[1].text)


def get_lift_stats(info, soup):
    lifts_table = soup.find('table', id='lifts').find('tbody')  # lift stats
    num_lifts = lifts_table.find('tr').find_all('td')[1].text
    info.append(num_lifts)


def get_ticket_info(info, soup):
    tickets_table = soup.find('table', class_='tickettable table').find('tbody')  # ticket pricing
    ticket_head = tickets_table.find('tr')
    adult = ticket_head.find('th', id='adult')
    adult_idx = int((ticket_head.index(adult) - 1) / 2)

    for row in tickets_table.find_all('tr')[1:]:
        if row.find('td').text == 'Regular':
            adult_ticket = row.find_all('td')[adult_idx].text  # adult regular pricing
            info.append(adult_ticket)


def get_resort_info(mountain_url):
    page = requests.get(mountain_url)
    soup = bs(page.text, 'html.parser')

    info = [soup.find('div', class_='resortname').text]  # resort name

    get_overview_stats(info, soup)
    get_lift_stats(info, soup)
    get_ticket_info(info, soup)

    table.append(info)


region_list = ['britishcolumbia', 'alberta', 'montana', 'idaho', 'wyoming', 'utah', 'colorado', 'california', 'nevada',
               'oregon', 'washington', 'arizona', 'newmexico', 'alaska']

table = []

start = time.time()
for region in ['newmexico']:
    mountain_urls = get_resort_urls(region)

    for url in mountain_urls:
        get_resort_info(url)
        print('Collected resort info for {}'.format(url))

print(table)
