import requests
from bs4 import BeautifulSoup,Tag
import pandas as pd
domain= 'https://indiankanoon.org'


html = requests.get('https://indiankanoon.org/browse/consumer/').text
soup = BeautifulSoup(html, 'lxml')
a_tags = soup.table.find_all('a')
years =[(a.text,a.get('href')) for a in a_tags]
years_data = []

for year in years:
    print('Extracting data for year:',year[0])
    year_data = requests.get(domain+year[1]).text
    year_soup = BeautifulSoup(year_data, 'lxml')
    a_tags = [a for a in year_soup.table.find_all('a') if a.text == 'Entire Year']
    if len(a_tags) == 0:
        continue

    years_data.append((year[0],a_tags[0].get('href')))


df = pd.DataFrame(years_data,columns=['year','link'])
df.to_csv('data/yearlinks.csv',index=False)

    

