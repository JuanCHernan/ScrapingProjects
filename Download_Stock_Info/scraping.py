import os
import requests
import pandas as pd
import numpy as np
from lxml import html
from urllib.request import urlopen
from requests_html import HTMLSession
from bs4 import BeautifulSoup

URL_web = 'https://www.investing.com'
URL_components = 'https://www.investing.com/indices/investing.com-us-500-components' 

# extract_companies will extract every components inside the S&P500
def extract_companies():
    data = requests.get(URL_components, 'html.parser')
    bs = BeautifulSoup(data.content, 'html.parser')
    table = bs.find("table", {'id':'cr1'}).find("tbody").find_all('tr')
    companies = []
    links = []
    for s in table:
        cell = s.find_all("td")[1].find("a")
        companies.append(cell['title'])
        links.append(URL_web+cell['href'])
    return companies, links

def extract_information(link):
    info = {}
    data = requests.get(link, 'html.parser')
    bs = BeautifulSoup(data.content, 'html.parser')
    table = bs.find_all('div', {'class': 'flex justify-between border-b py-2 desktop:py-0.5'})
    for i, t in enumerate(table):
        if i != 14:
            info[t.find('dt').text] = t.find_all('span')[0].find('span').text
        else:
            info[t.find('dt').text] = t.find('a').text
    return info

companies, links = extract_companies()
info = extract_information(links[2])
print(info)
