import requests
from bs4 import BeautifulSoup,Tag
import pandas as pd
domain= 'https://indiankanoon.org'


html = requests.get('https://indiankanoon.org/browse/consumer/').text
soup = BeautifulSoup(html, 'lxml')
td_tags = soup.table.find_all('td')
years =[(td.a.text.strip(),int(td.text.replace(td.a.text,'').replace('(','').replace(')','').strip())) for td in td_tags if td.a]



df = pd.DataFrame(years,columns=['year','count'])

print(df)
df.to_csv('data/year_data.csv',index=False)

    

