import collector
import processor
import analyser


AD_TYPES = [
    'prodaja', 
    'oddaja',
    ]
REAL_ESTATE_TYPES = [
    'stanovanje', 
    'hisa',
    ]
MAIN_PAGE = 'https://www.nepremicnine.net/'
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


def main():
    pages_to_download = processor.get_pages_to_download(ad_types=AD_TYPES, real_estate_types=REAL_ESTATE_TYPES, regions=REGIONS, main_page=MAIN_PAGE)    
    print(pages_to_download, len(pages_to_download))


if __name__ == '__main__':
    main()