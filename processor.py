import parser
import os
import collector
import csv


# Basic functions
def get_filename(page):
    """This function takes a link to a page as an argument 
    and returns the name of the file corresponding to this page."""
    filename = ''
    for components in page.split('/')[3:-1]:
        filename += components.lower() + '_'
    return filename[:-1]


def is_downloaded(directory, filename):
    """This function takes a file name as an argument and checks if it exists."""
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        return True
    else:
        return False


# Key functions
def get_url_base(ad_type, real_estate_type, region, main_page):
    """This function takes as an argument the basic parameters for the search 
    and returns a basic link to the first page with these parameters."""
    return f'{main_page}oglasi-{ad_type}/{region}/{real_estate_type}/'


def get_url_bases(ad_types, real_estate_types, regions, main_page):
    """This function takes as an argument the basic parameters for the search 
    and returns all links to first pages with these parameters."""
    url_bases = set()
    for ad_type in ad_types:
        for real_estate_type in real_estate_types:
            for region in regions:
                url_base = get_url_base(ad_type, real_estate_type, region, main_page)
                url_bases.add(url_base)
    return url_bases


def get_pages(url_bases, directory):
    """This function takes base links as an argument 
    and returns all links to all pages with the given parameters."""
    pages_to_download = set()

    for url_base in url_bases:
        number_of_pages = parser.get_number_of_pages(url_base, directory)        
        for number in range(1, number_of_pages + 1):
            page_to_download = f'{url_base}{number}/'
            pages_to_download.add(page_to_download)       
    return pages_to_download


def download_pages(pages, directory): 
    """This function takes page links as an argument and downloads them."""
    for page in pages:
        filename = get_filename(page)

        if is_downloaded(directory, filename):
            continue
        else:
            collector.save_page_to_file(page, directory, filename)


def get_ads_from_pages(pages, directory):
    """This function reads the data in pages and
    converts (parses) it into the corresponding dictionary list for each ad."""
    ads = []
    for page in pages:
        filename = get_filename(page)
        ads.extend(parser.get_ads(filename, directory))
    return ads


def write_ads_to_csv(ads, directory, csv_filename):
    """This function writes all data from the "ads" parameter to the csv file given by
    by the "directory"/"filename" parameters. The function assumes that the keys of all
    dictionary keys of the ads parameter are the same and the ads list is non-empty."""
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))

    fieldnames = list(ads[0].keys())
    
    write_csv(fieldnames, ads, directory, csv_filename)


def write_csv(fieldnames, rows, directory, filename):
    """This function writes to the csv file given by the parameters "directory"/"filename"
    the values in the "rows" parameter corresponding to the keys given in "fieldnames"."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)

    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def get_true_ads_from_ads(ads, directory, filename):
    """This function as an argument takes a list of all ads and 
    the location of the file given by the parameters "directory"/"filename"
    with id of fake ads and returns a list of only real ads."""
    true_ads = []
    
    id_of_fake_ads = get_id_of_fake_ads(directory, filename)

    for ad in ads:
        if not ad['ad_id'] in id_of_fake_ads:
            true_ads.append(ad)

    return true_ads 


def get_id_of_fake_ads(directory, filename):
    """This function as an argument takes the location of the file 
    given by the parameters "directory"/"filename"
    with id of fake ads and returns a set of id of fake ads."""
    id_of_fake_ads = set()
    
    path = os.path.join(directory, filename)    
    with open(path, 'r', encoding='utf-8') as file:
        for id_of_fake_ad in file:
            id_of_fake_ads.add(id_of_fake_ad.strip())
    
    return id_of_fake_ads


def is_fake_ad(ad_id, id_of_fake_ads):
    """This function takes as an argument the id of the ad and the set of id of 
    all fake ads and returns True if the ad is fake and False otherwise."""
    if ad_id in id_of_fake_ads:
        return True
    else:
        return False