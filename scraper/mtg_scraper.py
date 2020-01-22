# Load all packages necessary for analysis
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

# make a webcrawler to gather the data from mtgtop8.com on competitive decks
url = 'https://www.mtgtop8.com/format?f=ST&meta=52'
url_standard_page_response = requests.get(url)

# save the response
with open('url_standard_page_response.html', mode='wb') as file:
    file.write(url_standard_page_response.content)

# open response as a BeautifulSoup object
with open('url_standard_page_response.html') as file:
    soup = BeautifulSoup(file, 'lxml')

# find all urls for deck types and put them into a dataframe
url = {'url': soup.find_all(href=re.compile(r"archetype\?a"))}
deck_type_urls = pd.DataFrame(data=url)

# make deck_type_urls.url a string and extract types from it and name the column 'type'
deck_type_urls.url = deck_type_urls.url.astype('str')
deck_type_urls['type'] = deck_type_urls.url.str.extract('(>.+<)')

# clean up 'type' column
deck_type_urls.type = deck_type_urls.type.str.replace('>', '').str.replace('<', '').str.replace(' ', '_').str.replace('/', '-')

# extract url from url column and add base url to it and clean it up a bit
deck_type_urls.url = deck_type_urls.url.str.extract('(archetype\?a.+f\=ST)')
deck_type_urls.url = 'https://www.mtgtop8.com/' + deck_type_urls.url
deck_type_urls.url = deck_type_urls.url.str.replace('amp;', '')

# create web crawler to request html pages from deck_type_urls

# create new path and name it newpath
newpath = 'type_html_files'

# check to make sure that there is no path that matches newpath and create a folder called type_html_files if there isn't
if not os.path.exists(newpath):
    os.makedirs(newpath)

# change current directory to newpath
os.chdir(newpath)

# scrape all html files from urls in deck_type_urls and put them in type_html_files folder
for i in np.arange(deck_type_urls.shape[0]):
    type_html = requests.get(deck_type_urls.url[i])
    with open(deck_type_urls.type[i] + '.html', 'wb') as file:
        file.write(type_html.content)

# get a list of file names in type_html_files folder and name it dir_names
cur_dir = os.path.abspath(os.curdir)
dir_names = []

with os.scandir(cur_dir) as folder:
    for file in folder: 
        if file.is_file():
            dir_names.append(file.name)


# check to make sure that there is no path that matches cur_dir and create a folder called type_html_files if there isn't
if not os.path.exists(cur_dir):
    os.makedirs(cur_dir)

# change current directory to cur_dir
os.chdir(cur_dir)

# scrape all html files from urls in deck_type_urls and put them in type_html_files folder
for i in np.arange(deck_type_urls.shape[0]):
    type_html = requests.get(deck_type_urls.url[i])
    if not os.path.exists(str(cur_dir) + '/' + str(dir_names[i])):
        with open(deck_type_urls.type[i] + '.html', 'wb') as file:
            file.write(type_html.content)

# get a list of all urls in all files
players = []
urls = []

for i in np.arange(np.count_nonzero(dir_names)):
    with open(os.path.abspath(os.curdir) + '/' + dir_names[i], encoding='latin_1') as file:
        soup = BeautifulSoup(file, 'lxml')
    for a in soup.find_all(href=re.compile(r'search\?player')):
        players.append(a)
    for a in soup.find_all(href=re.compile(r'event\?e\=.+\&d\=.+\&f\=ST')):
        urls.append(a) 

# put players and urls into a dataframe
deck_urls = pd.DataFrame({'player': players, 
                         'url': urls})

# clean up player and url columns
deck_urls.player = deck_urls.player.astype('str')
deck_urls.player = deck_urls.player.str.extract('(>.+<)')
deck_urls.player = deck_urls.player.str.replace('>', '').str.replace('<', '').str.replace(' ', '_').str.replace('/', '-')

# extract names from urls and add them to name column and clean it up
deck_urls.url = deck_urls.url.astype('str')
names = deck_urls.url.str.extract('(>.+<)')
deck_urls['name'] = names
deck_urls.name = deck_urls.name.str.replace('>', '').str.replace('<', '').str.replace(' ', '_').str.replace('/', '-')

# clean up url column
deck_urls.url = deck_urls.url.str.extract('(event.+f\=ST)')
deck_urls.url = deck_urls.url.str.replace('amp;', '')

# add url root to url column
deck_urls.url = 'https://www.mtgtop8.com/' + deck_urls.url

# back up one folder
os.chdir('..')

# create new path and name it newpath
newpath = os.path.abspath(os.curdir) + 'html_files'

# check to make sure that there is no path that matches newpath and create a folder called type_html_files if there isn't
if not os.path.exists(newpath):
    os.makedirs(newpath)

# change current directory to newpath
os.chdir(newpath)

# scrape all html files from urls in deck_urls and put them in html_files folder
deck_errors = []

for i in np.arange(deck_urls.shape[0]):
    try:
        deck_html = requests.get(deck_urls.url[i])
        if not os.path.exists(str(deck_urls.name[i]) + '_' + str(deck_urls.player[i] + '.html')):
            with open(str(deck_urls.name[i]) + '_' + str(deck_urls.player[i]) + '.html', 'wb') as file:
                file.write(deck_html.content)
    except Exception as e:
        print(str(i) + ' ' + str(e))
        deck_errors.append(i)

# get all directory names and put them in a list
dir_names = []

with os.scandir(newpath) as folder:
    for file in folder:
        if file.is_file():
            dir_names.append(file.name)

# take names and add them to curdir and open them and find cards and players with beautifulsoup 
deck_lists = []
players = []

for i in np.arange(np.count_nonzero(dir_names)):
    with open(str(newpath) + '/' + str(dir_names[i])) as file:
        soup = BeautifulSoup(file, 'lxml')
    deck_list = soup.find(lambda tag: tag.name=='input' and tag.has_attr('name') and tag['name']=='c')
    player = soup.find(lambda tag: tag.name=='a' and tag.has_attr('class'))
    deck_lists.append(deck_list)
    players.append(player)

deck_lists = pd.DataFrame({'deck_list': deck_lists, 
                           'players': players})

os.chdir('..')
deck_lists.to_csv('deck_lists.csv', index=False)
