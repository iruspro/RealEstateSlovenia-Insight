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
            continue
        processed_ads.append(processed_ad)
    return processed_ads

def get_ads_from_text(text):
    ad_template = r'<div class="property-box.*?>.*?</div>\s*</div>\s*</div>\s*</div>'
    ads = re.findall(ad_template, text, re.DOTALL)
    return ads

def get_dict_from_ad_block(block):  
    base_data = get_base_date_from_(block)  
    if base_data == None:
        return None

    ad_id = get_ad_id_from_(block)
    type_ = get_type_from_(block)    
    land_area = get_land_area_from_(block)
    living_area = get_living_area_from_(block)
    building_year = get_building_year_from_(block)
    floor = get_floor_from_(block)
    price = get_price_from_(block)
    seller = get_seller_from_(block)
    city = get_city_from_(block, base_data[1])

    if ad_id == None or city == None or living_area == None or price == None:
        return None  

    return {
        'ad_id': ad_id,
        'ad_type': base_data[0],
        'region': base_data[1],
        'real_estate_type': base_data[2],               
        'type': type_,
        'land_area': land_area,
        'city': city,
        'living_area': living_area,
        'building_year': building_year,
        'floor': floor,
        'price': price,
        'seller': seller,
    }

def get_base_date_from_(block):
    template_base_data = r'<meta itemprop="category" content="(.*?)/>'
    base_data = re.search(template_base_data, block)

    if base_data == None:
        return None
    else:
        base_data = base_data.group(1).split('>')
        if len(base_data) < 3:
            return None
        ad_type = base_data[0].split(' ')[1]
        region = base_data[1].strip()
        real_estate_type = 'hiša' if 'hisa' in base_data[2] else 'stanovanje'

    return ad_type, region, real_estate_type

def get_ad_id_from_(block):
    template_id = r'<div class="property-details".*?_(.*?)/">'
    ad_id = re.search(template_id, block)

    if ad_id == None:
        return None
    else:
        return ad_id.group(1)

def get_type_from_(block):
    template_type = r'<span class="tipi">(.*?)</span>'
    type_ = re.search(template_type, block)
    if type_ == None:
        return None
    else:
        return type_.group(1).lower()

def get_land_area_from_(block):
    template_land_area = r'<li><img src="https://www\.nepremicnine\.net/images/zemljisce\.svg".*?>(.*?) m<sup>2</sup></li>'
    land_area = re.search(template_land_area, block)
    if land_area == None:
        return 0
    else:
        return land_area.group(1)

def get_city_from_(block, region):
    if region == 'ljubljana mesto':
        return 'ljubljana'
    else:     
        template_city = r'<h2>(.*?)</h2>'
        city = re.search(template_city, block)
        if city == None:
            return None
        else:
            return city.group(1).split(',')[0].lower()

def get_living_area_from_(block):
    template_living_area = r'<li><img src="https://www\.nepremicnine\.net/images/velikost\.svg".*?>(.*?) m<sup>2</sup></li>'
    living_area = re.search(template_living_area, block)
    if living_area == None:
        return None
    else:
        return living_area.group(1)

def get_building_year_from_(block):
    template_building_year = r'<li><img src="https://www\.nepremicnine\.net/images/leto\.svg".*?>(.*?)</li>'
    building_year = re.search(template_building_year, block)
    if building_year == None:
        return None
    else:
        return building_year.group(1)

def get_floor_from_(block):
    template_floor = r'<li><img src="https://www\.nepremicnine\.net/images/nadstropje\.svg".*?>(.*?)</li>'
    floor = re.search(template_floor, block)
    if floor == None:
        return None
    else:
        return floor.group(1)

def get_price_from_(block):    
    template_price = r'<meta itemprop="price" content="(.*?)" />'
    price = re.search(template_price, block)
    if price == None:
        return None
    else:
        return price.group(1)

def get_seller_from_(block):
    template_seller = r'<meta itemprop="name" content="(.*?)" />'
    seller = re.search(template_seller, block)
    if seller == None:
        return None
    else:
        return seller.group(1)