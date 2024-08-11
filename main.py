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
    pages = processor.get_pages(url_bases)    
    processor.download_pages(pages)

    ads = processor.get_ads_from_pages(pages)
    processor.write_ads_to_csv(ads, 'data', 'ads.csv')


if __name__ == '__main__':
    main()