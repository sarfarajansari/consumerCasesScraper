import requests
from bs4 import BeautifulSoup,Tag
from datetime import datetime
from threading import Thread
import pandas as pd
domain= 'https://indiankanoon.org'
import time



data = []
threads = []

judgement_links = pd.read_csv('data/judgement_links.csv').values.tolist()

def get_judgement_data(item,attempt=0):
    try:
        title,link,full_url,year = item
        res = requests.get(link)

        if res.status_code != 200:
            print('Error:',res.status_code,res.text)
            print("Waiting for 10 seconds")

            if attempt>3:
                print('Attempt limit reached:',attempt)
                return
            time.sleep(10)
            return get_judgement_data(item,attempt+1)
        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        judgement_div:Tag = soup.select_one('.judgments')
        if not judgement_div:
            return
        judgement_div.select_one('.ad_doc').clear()
        judgement_div.select_one('h2.docsource_main').clear()
        text = judgement_div.text.strip()


        reference = [{
            'title':a.text,
            'link':domain + a.get('href')
        } for a in judgement_div.find_all('a')]

        data.append({
            'title':title,        
            'text':text,
            'html':str(judgement_div),
            'reference':reference,
            'year':year,
            'document_link':link,
            'search_url':full_url,
            'scrapped_at':datetime.now().isoformat()
        })

    except Exception as e:
        print(e)
        print(item)
        print('-------------------')

        if attempt>3:
            print('Attempt limit reached:',attempt)
            return
        time.sleep(10)
        return get_judgement_data(item,attempt+1)



for item in judgement_links:
    if len(threads) > 5:
        for t in threads:
            t.join()
        threads.clear()

    t = Thread(target=get_judgement_data,args=(item,))
    t.start()
    
    threads.append(t)
    
for t in threads:
    t.join()

    
print(len(data))

data.sort(key=lambda x:int(x['year']))

data.reverse()

import json
with open('data/consumer_cases.json','w') as f:
    json.dump(data,f,indent=4)


df = pd.DataFrame(data)
df.to_csv('data/consumer_cases.csv',index=False)