import requests
from bs4 import BeautifulSoup as bs
import time


def get_resort_urls():
    """ Adjust the region list below if desired. Use skicentral.com to see which regions are available."""

    region_list = ['britishcolumbia', 'alberta', 'montana', 'idaho', 'wyoming', 'utah', 'colorado', 'california',
                   'nevada', 'oregon', 'washington', 'arizona', 'newmexico', 'alaska']

    resort_urls = []

    for region in region_list:
        base_url = 'https://www.skicentral.com/'
        full_url = base_url + region + '.html'

        page = requests.get(full_url)
        soup = bs(page.text, 'html.parser')

        for resort in soup.find_all('div', class_='resorttitle'):
            link = resort.find('a')
            resort_urls.append(base_url + link['href'])

        time.sleep(1)

    return resort_urls


def get_resort_address(info, soup):
    try:
        contact = soup.find('div', class_='addressblock')
        address = contact.text.split('Email:')[0].split('Address:')[1].strip()
        info.append(address)

    except AttributeError:
        info.append(None)


def get_overview_stats(info, soup):
    overview_table = soup.find('table', id='mountainstatistics').find('tbody')  # main mountain stats

    for row in overview_table.find_all('tr')[:8]:
        info.append(row.find_all('td')[1].text)


def get_lift_stats(info, soup):
    lifts_table = soup.find('table', id='lifts').find('tbody')  # lift stats
    num_lifts = lifts_table.find('tr').find_all('td')[1].text
    info.append(num_lifts)


def get_ticket_info(info, soup):
    try:
        tickets_table = soup.find('table', class_='tickettable table').find('tbody')

        for row in tickets_table.find_all('tr'):
            if row.find('td') is not None:  # check that the row is not the header
                if row.find('td').text == 'Regular':
                    max_price = None
                    for col in row.find_all('td')[1:]:
                        price = int(col.text.split('$')[1])
                        if max_price is None or price > max_price:
                            max_price = price
                    info.append(max_price)

    except AttributeError:
        info.append(None)


def clean(info):
    for idx, col in enumerate(info):
        if (2 <= idx < 6) and (col != 'n/a' or col is not None):
            info[idx] = col.split()[0]


def get_resort_info(mountain_url):
    page = requests.get(mountain_url)
    soup = bs(page.text, 'html.parser')

    info = [soup.find('div', class_='resortname').text]  # resort name

    get_resort_address(info, soup)
    get_overview_stats(info, soup)
    get_lift_stats(info, soup)
    get_ticket_info(info, soup)

    clean(info)

    table.append(info)


table = []
start = time.time()

mountain_urls = get_resort_urls()
print('Collected URLs for {} ski resorts.'.format(len(mountain_urls)))

for url in mountain_urls:
    get_resort_info(url)
    time.sleep(1)

print('Collected resort info for {} ski resorts'.format(len(table)))
print('Completed scraping in: {}'.format(time.time() - start))
