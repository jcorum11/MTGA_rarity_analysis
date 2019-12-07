# Load all packages necessary for analysis
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import timeit
import filecmp

# pull deck type urls from mtgtop8.com with requests package
url = 'https://www.mtgtop8.com/format?f=ST'
url_standard_page_response = requests.get(url)

# save the response
with open('C:\\Users\\muroc\\Documents\\MTG\\data\\url_standard_page_response.html', mode='wb') as file:
    file.write(url_standard_page_response.content)

# open response as a BeautifulSoup object
with open('C:\\Users\\muroc\\Documents\\MTG\\data\\url_standard_page_response.html') as file:
    soup = BeautifulSoup(file, 'lxml')

# make the urls pulled from mtgtop8.com a dataframe with each observation a different url
url = {'url': soup.find_all(href=re.compile(r"archetype\?a"))}
deck_type_urls = pd.DataFrame(data=url)

# create column for deck type and clean the column
url_stripper.url_stripper(deck_type_urls, 'url', 'type', '(>.+<)')
deck_type_urls['url'] = deck_type_urls.url.str.extract('(archetype.+f\=ST)')

# add root url to the data
urls = []
for i in np.arange(deck_type_urls.shape[0]):
    urls.append(str('https://www.mtgtop8.com/') + deck_type_urls.url[i])

# clean up url column
deck_type_urls['url'] = urls
deck_type_urls['type'] = deck_type_urls.type.str.replace(' ', '_')
deck_type_urls['type'] = deck_type_urls.type.str.replace('/', '-')

# create web crawler to request html pages from deck_type_urls
# create new path and name it newpath
newpath = 'C:\\Users\\muroc\\Documents\\MTG\\type_html_files'

# check to make sure that there is no path that matches newpath and create a folder called html_files if there isn't
if not os.path.exists(newpath):
    os.makedirs(newpath)

# change current directory to newpath
os.chdir(newpath)

# scrape all html files from urls in deck_type_urls and put them in html_files folder
for i in np.arange(deck_type_urls.shape[0]):
    type_html = requests.get(deck_type_urls.url[i])
    with open(deck_type_urls.type[i], 'wb') as file:
        file.write(type_html.content)

# get a list of file names in type_html_files folder and name it dir_names
dir_names = []
cur_dir = 'C:/Users/muroc/Documents/MTG/type_html_files/'

with os.scandir(cur_dir) as folder:
    for file in folder: 
        if file.is_file():
            dir_names.append(file.name)

# get player names
players = []
with open('C:/Users/muroc/Documents/MTG/type_html_files/4-5c_Aggro.html') as file:
    soup = BeautifulSoup(file, 'lxml')
for a in soup.find_all(href=re.compile(r'search\?player')):
    players.append(a)