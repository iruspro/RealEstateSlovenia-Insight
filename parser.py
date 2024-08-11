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
        collector.save_page_to_file(url_base, directory=DIRECTORY, filename=filename)
        
    text = read_file_to_string(directory=DIRECTORY, filename=filename)
    number_of_pages = get_number_of_pages_from_text(text)
    return number_of_pages
    

def get_number_of_pages_from_text(text):
    template_number_of_pages = r'<li class="paging_last"><a href=(.*?) class="last">>></a></li>'
    number_of_pages = re.search(template_number_of_pages, text)
    
    if number_of_pages != None:
        return int(number_of_pages.group(1).split('/')[4])
    else:
        return 1
