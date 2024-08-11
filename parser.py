import re
import collector
import os
import processor


# Basic function
def read_file_to_string(directory, filename):
    """The function takes a directory and a file as an argument and returns the contents of the file as a string."""
    filepath = os.path.join(directory, filename)    
    with open(filepath, 'r', encoding='UTF-8') as file:
        text = file.read()
    return text


# Main functions
def get_number_of_pages(url_base, directory):
    """The function takes as an argument the base link and 
    the directory to save the base page and returns the number of pages with these parameters."""
    filename = processor.get_filename(url_base) + '_1'

    if not processor.is_downloaded(filename, directory):
        collector.save_page_to_file(url_base, directory, filename)

    text = read_file_to_string(directory, filename)
    number_of_pages = get_number_of_pages_from_text(text)
    return number_of_pages
    

def get_number_of_pages_from_text(text):
    """The function takes text as an argument and extracts from it 
    the number of pages with the given parameters."""
    template_number_of_pages = r'<li class="paging_last"><a href=(.*?) class="last">>></a></li>'
    number_of_pages = re.search(template_number_of_pages, text)
    
    if number_of_pages != None:
        return int(number_of_pages.group(1).split('/')[4])
    else:
        return 1


def get_ads(filename, directory):
    """The function takes as an argument the name of the file 
    and the directory where it is located and returns all the ads 
    located in this file as a list of dictionaries with the necessary data."""
    processed_ads = []    
    text = read_file_to_string(directory, filename)
    blocks = get_ads_from_text(text)
    for block in blocks:
        processed_ad = get_dict_from_ad_block(block)
        if processed_ad == None:
            continue
        processed_ads.append(processed_ad)
    return processed_ads


def get_ads_from_text(text):
    """This function searches for individual ads located on the website and
    returns a list of ads."""
    ad_template = r'<div class="property-box.*?>.*?</div>\s*</div>\s*</div>\s*</div>'
    ads = re.findall(ad_template, text, re.DOTALL)
    return ads


def get_dict_from_ad_block(block):  
    """The function extracts from ad block the ad id, ad type, region, 
    real estate type (flat or house), type, land area, city, living area, building year, floor,
    price and seller and returns a dictionary containing the relevant data."""
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


def was_found(match):
    """The function takes a search object as an argument and returns its contents 
    or None if no match was found."""
    if match == None:
        return None
    else:
        return match.group(1).lower()


def get_base_date_from_(block):
    """The function takes a block with a ad as an argument 
    and returns basic data about it or None if there is no necessery data in the block."""
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
    """The function takes a block with a ad as an argument 
    and returns ad id or None if there is no ad id in the block."""
    template_id = r'<div class="property-details".*?_(.*?)/">'
    ad_id = re.search(template_id, block)
    return was_found(ad_id)


def get_type_from_(block):
    """The function takes a block with a ad as an argument 
    and returns type or None if there is no type in the block."""
    template_type = r'<span class="tipi">(.*?)</span>'
    type_ = re.search(template_type, block)
    return was_found(type_)


def get_land_area_from_(block):
    """The function takes a block with a ad as an argument 
    and returns land area or None if there is no land area in the block."""
    template_land_area = r'<li><img src="https://www\.nepremicnine\.net/images/zemljisce\.svg".*?>(.*?) m<sup>2</sup></li>'
    land_area = re.search(template_land_area, block)
    return was_found(land_area)


def get_city_from_(block, region):
    """The function takes a block with a ad as an argument 
    and returns city or None if there is no city in the block."""
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
    """The function takes a block with a ad as an argument 
    and returns living area or None if there is no living area in the block."""
    template_living_area = r'<li><img src="https://www\.nepremicnine\.net/images/velikost\.svg".*?>(.*?) m<sup>2</sup></li>'
    living_area = re.search(template_living_area, block)
    return was_found(living_area)


def get_building_year_from_(block):
    """The function takes a block with a ad as an argument 
    and returns building year or None if there is no building year in the block."""
    template_building_year = r'<li><img src="https://www\.nepremicnine\.net/images/leto\.svg".*?>(.*?)</li>'
    building_year = re.search(template_building_year, block)
    return was_found(building_year)


def get_floor_from_(block):
    """The function takes a block with a ad as an argument 
    and returns floor or None if there is no floor in the block."""
    template_floor = r'<li><img src="https://www\.nepremicnine\.net/images/nadstropje\.svg".*?>(.*?)</li>'
    floor = re.search(template_floor, block)
    return was_found(floor)


def get_price_from_(block):    
    """The function takes a block with a ad as an argument 
    and returns price or None if there is no price in the block."""
    template_price = r'<meta itemprop="price" content="(.*?)" />'
    price = re.search(template_price, block)
    return was_found(price)


def get_seller_from_(block):
    """The function takes a block with a ad as an argument 
    and returns seller or None if there is no seller in the block."""
    template_seller = r'<meta itemprop="name" content="(.*?)" />'
    seller = re.search(template_seller, block)
    return was_found(seller)