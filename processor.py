import parser


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

def get_page_links(url_bases):
    pages_to_download = set()

    for url_base in url_bases:
        number_of_pages = parser.get_number_of_pages(url_base)        
        for number in range(1, number_of_pages + 1):
            page_to_download = f'{url_base}{number}/'
            pages_to_download.add(page_to_download)       
    return pages_to_download