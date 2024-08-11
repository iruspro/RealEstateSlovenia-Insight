import collector


def get_url_base(ad_type, real_estate_type, region, main_page):
    return f'{main_page}oglasi-{ad_type}/{region}/{real_estate_type}/'

def get_url_bases(ad_types, real_estate_types, regions, main_page):
    url_bases = set()
    for ad_type in ad_types:
        for real_estate_type in real_estate_types:
            for region in regions:
                url_base = get_url_base(ad_type, real_estate_type, region, main_page)
                url_bases.add(first_page)
    return url_bases

def get_number_of_pages(first_page):
    filename = get_filename(first_page)
    collector.save_page_to_file(first_page, 'pages', filename)
    return 1

def get_pages_to_download(ad_types, real_estate_types, regions, main_page):
    pages_to_download = set()
    
    first_pages = get_first_pages(ad_types, real_estate_types, regions, main_page)
    for first_page in first_pages:
        number_of_pages = get_number_of_pages(first_page)
        for number in range(1, number_of_pages + 1):
            page_to_download = f'{first_page}{number}/'
            pages_to_download.add(page_to_download)    
    
    return pages_to_download


def get_filename(link):
    filename = ''
    for data in link.split('/')[3:-1]:
        filename += data.lower() + '_'

    return filename[:-1]
