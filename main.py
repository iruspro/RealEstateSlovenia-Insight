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
PAGES_DIRECTORY = 'pages'
DATA_DIRECTORY = 'data'
DATA_FILENAME = 'ads.csv'
FAKE_ADS_FILENAME = 'fake_ads'


def main():
    url_bases = processor.get_url_bases(
        ad_types=AD_TYPES, 
        real_estate_types=REAL_ESTATE_TYPES, 
        regions=REGIONS, 
        main_page=MAIN_PAGE)    
    pages = processor.get_pages(url_bases, PAGES_DIRECTORY)    
    processor.download_pages(pages, PAGES_DIRECTORY)

    ads = processor.get_ads_from_pages(pages, PAGES_DIRECTORY)
    true_ads = processor.get_true_ads_from_ads(ads, DATA_DIRECTORY, FAKE_ADS_FILENAME)
    processor.write_ads_to_csv(true_ads, DATA_DIRECTORY, DATA_FILENAME)


if __name__ == '__main__':
    main()