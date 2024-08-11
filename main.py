import processor


AD_TYPES = [
    'prodaja', 
    'oddaja',
    ]
REAL_ESTATE_TYPES = [
    'stanovanje', 
    'hisa',
    ]
REGIONS = [
    'ljubljana-mesto', 
    'ljubljana-okolica', 
    'gorenjska', 
    'juzna-primorska', 
    'severna-primorska', 
    'notranjska', 
    'savinjska', 
    'podravska', 
    'koroska', 
    'dolenjska', 
    'posavska', 
    'zasavska', 
    'pomurska',
    ]
MAIN_PAGE = 'https://www.nepremicnine.net/'


def main():
    url_bases = processor.get_url_bases(
        ad_types=AD_TYPES, 
        real_estate_types=REAL_ESTATE_TYPES, 
        regions=REGIONS, 
        main_page=MAIN_PAGE)
    
    page_links = processor.get_page_links(url_bases)
    
    processor.download_pages(page_links)


if __name__ == '__main__':
    main()