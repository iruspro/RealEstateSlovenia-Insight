import re
import collector
import os


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


