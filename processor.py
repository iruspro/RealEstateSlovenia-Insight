import parser
import os
import collector
import csv


DIRECTORY = 'pages'


# Key functions
def get_url_base(ad_type, real_estate_type, region, main_page):
    return f'{main_page}oglasi-{ad_type}/{region}/{real_estate_type}/'

def get_url_bases(ad_types, real_estate_types, regions, main_page):
    url_bases = set()
    for ad_type in ad_types:
        for real_estate_type in real_estate_types:
            for region in regions:
                url_base = get_url_base(ad_type, real_estate_type, region, main_page)
                url_bases.add(url_base)
    return url_bases

def get_pages(url_bases):
    pages_to_download = set()

    for url_base in url_bases:
        number_of_pages = parser.get_number_of_pages(url_base)        
        for number in range(1, number_of_pages + 1):
            page_to_download = f'{url_base}{number}/'
            pages_to_download.add(page_to_download)       
    return pages_to_download

def download_pages(page_links): 
    for page_link in page_links:
        filename = parser.get_filename(page_link)

        if is_downloaded(filename):
            continue
        else:
            collector.save_page_to_file(page_link, DIRECTORY, filename)


def is_downloaded(filename):
    filepath = os.path.join(DIRECTORY, filename)
    if os.path.exists(filepath):
        return True
    else:
        return False

def get_ads_from_pages(pages):
    ads = []

    for page in pages:
        filename = parser.get_filename(page)
        ads.extend(parser.get_ads(filename))
    return ads

def write_ads_to_csv(ads, directory, csv_filename):
    fieldnames = list(ads[0].keys())
    write_csv(fieldnames, ads, directory, csv_filename)
    
def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

