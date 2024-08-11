import requests
import os


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 
    'authority': 'www.nepremicnine.net'}


def download_url_to_string(url):
    """The function takes a url-string as an argument and tries to return the contents of this web
    as a string. If an error occurs during execution, it returns None.
    """
    try:
        page_content = requests.get(url, headers=HEADERS)        
    except requests.exceptions.RequestException:
        return None    
    return page_content.text


def save_string_to_file(text, directory, filename):
    """The function writes the value of the "text" parameter to a newly created file
    located in "directory"/"filename", or overwrites an existing one. In case
    the "directory" string is empty, the file is created in the current directory.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)

    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)    
    return None


def save_page_to_file(page, directory, filename):
    """This function saves the content of the web-page at address "page" to a file
    "directory"/"filename"."""
    text = download_url_to_string(page)
    save_string_to_file(text, directory, filename)