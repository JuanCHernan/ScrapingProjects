import os
import requests
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup

URL_web = 'https://www.investing.com'
URL_components = 'https://www.investing.com/indices/investing.com-us-500-components' 

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

companies, links = extract_companies()
data = requests.get(links[0], 'html.parser')
bs = BeautifulSoup(data.content, 'html.parser')
print(bs)
