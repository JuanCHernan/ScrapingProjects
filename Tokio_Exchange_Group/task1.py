import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

URL = "https://www2.jpx.co.jp/tseHpFront/JJK020010Action.do?Show=Show"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)

##### Apply Filters #####
select = Select(driver.find_element_by_xpath('//*[@id="bodycontents"]/div[2]/form/div[1]/table/tbody/tr[1]/td/span/select'))
select.select_by_visible_text('200')
driver.find_element_by_xpath('//*[@id="bodycontents"]/div[2]/form/div[1]/table/tbody/tr[4]/td/span/span/label[1]').click()
driver.find_element_by_xpath('//*[@id="bodycontents"]/div[2]/form/p/input').click()

##### Extract Info #####
def extract_info(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table').find_all('tr')
    information = {
            'code':[],
            'issue':[],
            'market_segment':[],
            'industry':[],
            'fiscal':[],
            'alert':[]}

    for tr in table[2:]:
        tds = tr.find_all('td')[:6]
        information['code'].append(tds[0].text.strip())
        information['issue'].append(tds[1].text.strip())
        information['market_segment'].append(tds[2].text.strip())
        information['industry'].append(tds[3].text.strip())
        information['fiscal'].append(tds[4].text.strip())
        information['alert'].append(tds[5].text.strip())
    dataFrame = pd.DataFrame(information)
    return dataFrame

##### Iterate over pages and extract info#####
data = []
for i in range(10):
   dataFrame = extract_info(driver)
   data.append(dataFrame)
   if i != 9:
       driver.find_element_by_xpath('//*[@id="bodycontents"]/div[2]/form/div[1]/div[2]/a/img').click()

fDataFrame = pd.concat(data)
print(fDataFrame.shape)
