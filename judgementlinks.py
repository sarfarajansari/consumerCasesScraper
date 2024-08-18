import requests
from bs4 import BeautifulSoup,Tag
from datetime import datetime
from threading import Thread
import pandas as pd
domain= 'https://indiankanoon.org'

import time
from threading import Thread


threads = []

search_links = pd.read_csv('data/searchlinks.csv').values.tolist()

judgement_links = []


def join_url(url):
    if url.startswith('/'):
        return domain + url
    if url.startswith('http'):
        return url
    
    return domain + '/' + url


def get_data(search_id,url,page=1,attempt=0):
    print(f'{page}.Extracting data for year:',search_id)
    full_url =join_url(url)
    res = requests.get(full_url)

    if res.status_code != 200:
        print('Error:',res.status_code,res.text)
        print("Waiting for 10 seconds")

        if attempt>3:
            print('Attempt limit reached:',attempt)
            return
        time.sleep(10)
        return get_data(search_id,url,page,attempt+1)
    data = res.text
    soup = BeautifulSoup(data, 'lxml')


    results = soup.select('.results_middle .result .result_title > a')
    
    for result in results:
        title = result.text
        link = domain + result.get('href')
        judgement_links.append((title,link,full_url,search_id))

    
    next = [a.get('href') for a in soup.select('.bottom > a') if a.text == 'Next']

    




    

    if len(next) > 0:
        # print('Next page:',domain + next[0])
        return get_data(search_id, next[0],page+1,attempt=attempt)
    
    
    if page==40:
        print('No more pages for id:',search_id, 'last page:',page)







for searchitem in search_links:

    if len(threads)>5:
        for t in threads:
            t.join()
        threads.clear()


    t = Thread(target=get_data,args=(searchitem[0],searchitem[1]))
    t.start()
    threads.append(t)
    


for t in threads:
    t.join()


df = pd.DataFrame(judgement_links,columns=['title','link','full_url','year'])
df.to_csv('data/judgement_links.csv',index=False)