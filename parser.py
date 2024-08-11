import re
import collector
import os
import processor


DIRECTORY = 'pages'


# Basic function
def read_file_to_string(directory, filename):
    filepath = os.path.join(directory, filename)    
    with open(filepath, 'r', encoding='UTF-8') as file:
        text = file.read()
    return text

def get_filename(url):
    filename = ''
    for data in url.split('/')[3:-1]:
        filename += data.lower() + '_'

    return filename[:-1]


# Main functions
def get_number_of_pages(url_base):
    filename = get_filename(url_base) + '_1'

    if not processor.is_downloaded(filename):
        collector.save_page_to_file(url_base, DIRECTORY, filename)

    text = read_file_to_string(DIRECTORY, filename)
    number_of_pages = get_number_of_pages_from_text(text)
    return number_of_pages
    

def get_number_of_pages_from_text(text):
    template_number_of_pages = r'<li class="paging_last"><a href=(.*?) class="last">>></a></li>'
    number_of_pages = re.search(template_number_of_pages, text)
    
    if number_of_pages != None:
        return int(number_of_pages.group(1).split('/')[4])
    else:
        return 1

def get_ads(filename):
    processed_ads = []    
    text = read_file_to_string(DIRECTORY, filename)
    blocks = get_ads_from_text(text)
    for block in blocks:
        processed_ad = get_dict_from_ad_block(block)
        if processed_ad == None:
            print(filename)
            continue
        processed_ads.append(processed_ad)
    return processed_ads

def get_ads_from_text(text):
    ad_template = r'<div class="property-box.*?>.*?</div>\s*</div>\s*</div>\s*</div>'
    ads = re.findall(ad_template, text, re.DOTALL)
    return ads

def get_dict_from_ad_block(block):
    template_base_data = r'<meta itemprop="category" content="(.*?)/>'
    template_id = r'<div class="property-details".*?_(.*?)/">'
    template_type = r'<span class="tipi">(.*?)</span>'
    template_land_area = r'<li><img src="https://www\.nepremicnine\.net/images/zemljisce\.svg".*?>(.*?) m<sup>2</sup></li>'
    template_city = r'<h2>(.*?)</h2>'
    template_living_area = r'<li><img src="https://www\.nepremicnine\.net/images/velikost\.svg".*?>(.*?) m<sup>2</sup></li>'
    template_building_year = r'<li><img src="https://www\.nepremicnine\.net/images/leto\.svg".*?>(.*?)</li>'
    template_floor = r'<li><img src="https://www\.nepremicnine\.net/images/nadstropje\.svg".*?>(.*?)</li>'
    template_price = r'<meta itemprop="price" content="(.*?)" />'
    template_seller = r'<meta itemprop="name" content="(.*?)" />'

    base_data = re.search(template_base_data, block)
    if base_data == None:
        return None
    else:
        base_data = base_data.group(1).split('>')
        if len(base_data) < 3:
            return None
        ad_type = base_data[0].split(' ')[1]
        region = base_data[1].strip()
        real_estate_type = 'hiša' if 'hisa' in base_data[1].strip() else 'stanovanje' 

    ad_id = re.search(template_id, block)
    type_ = re.search(template_type, block)
    land_area = re.search(template_land_area, block)
    city = re.search(template_city, block)
    living_area = re.search(template_living_area, block)
    building_year = re.search(template_building_year, block)
    floor = re.search(template_floor, block)
    price = re.search(template_price, block)
    seller = re.search(template_seller, block)

    if ad_id == None:
        return None

    if land_area == None:
        land_area = 0
    else:
        land_area = land_area.group(1)

    if region == 'ljubljana mesto':
        city = 'ljubljana'
    else:
        city = city.group(1).split(',')[0]

    if living_area == None:
        return None
    else:
        living_area = living_area.group(1)        

    if floor == None:
        floor = 'no info'
    else:
        floor = floor.group(1)

    return {
        'ad_type': ad_type,
        'region': region,
        'real_estate_type': real_estate_type,
        'ad_id': ad_id.group(1),
        'type': type_.group(1),
        'land_area': land_area,
        'city': city,
        'living_area': living_area,
        'building_year': building_year.group(1),
        'floor': floor,
        'price': price.group(1),
        'seller': seller.group(1),
    }


