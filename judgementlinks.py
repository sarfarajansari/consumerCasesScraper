import requests
from bs4 import BeautifulSoup,Tag
from datetime import datetime
from threading import Thread
import pandas as pd
domain= 'https://indiankanoon.org'


from threading import Thread


threads = []

years_data = pd.read_csv('data/yearlinks.csv').values.tolist()

judgement_links = []


def join_url(url):
    if url.startswith('/'):
        return domain + url
    if url.startswith('http'):
        return url
    
    return domain + '/' + url


def get_data(year,url,page=1):
    print(f'{page}.Extracting data for year:',year)
    full_url =join_url(url)
    data = requests.get(full_url).text
    soup = BeautifulSoup(data, 'lxml')


    results = soup.select('.results_middle .result .result_title > a')
    
    for result in results:
        title = result.text
        link = domain + result.get('href')
        judgement_links.append((title,link,full_url,year))

    
    next = [a.get('href') for a in soup.select('.bottom > a') if a.text == 'Next']

    

    if len(next) > 0:
        # print('Next page:',domain + next[0])
        return get_data(year, next[0],page+1)
    
    print('No more pages for year:',year, 'last page:',page)









for year in years_data:

    if len(threads)>5:
        for t in threads:
            t.join()
        threads.clear()


    t = Thread(target=get_data,args=(year[0],year[1]))
    t.start()
    threads.append(t)
    


for t in threads:
    t.join()


df = pd.DataFrame(judgement_links,columns=['title','link','full_url','year'])
df.to_csv('data/judgement_links.csv',index=False)