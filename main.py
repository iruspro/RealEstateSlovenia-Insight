import collector
import processor
import analyser


AD_TYPES = ['prodaja', 'oddaja']
REAL_ESTATE_TYPES = ['stanovanje', 'hisa']
MAIN_PAGE = 'https://www.nepremicnine.net/'
REGIONS = ['LJ-mesto', 'LJ-okolica', 'Gorenjska', 'J. Primorska', 'S.Primorska', 'Notranjska', 'Savinjska', 'Podravska', 'Koroška', 'Dolenjska', 'Posavska', 'Zasavska', 'Pomurska']


def main():
    collector.save_page_to_file(MAIN_PAGE, 'pages', 'main_page')

if __name__ == '__main__':
    main()