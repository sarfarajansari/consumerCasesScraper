from db import insert_data
import time
import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from threading import Thread
import pandas as pd
domain = 'https://indiankanoon.org'


data = []
threads = []

judgement_links = pd.read_csv('data/judgement_links.csv').values.tolist()


def get_judgement_data(item, index, attempt=0):
    try:
        title, link, full_url, year = item
        res = requests.get(link)

        if res.status_code != 200:
            print('Error:', res.status_code, title,"Waiting for 30 seconds")

            if attempt > 3:
                print('Attempt limit reached:', attempt)
                return
            time.sleep(30)
            return get_judgement_data(item, index, attempt+1)
        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        judgement_div: Tag = soup.select_one('.judgments')
        if not judgement_div:
            return
        judgement_div.select_one('.ad_doc').clear()
        judgement_div.select_one('h2.docsource_main').clear()
        text = judgement_div.text.strip()

        reference = [{
            'title': a.text,
            'link': domain + a.get('href')
        } for a in judgement_div.find_all('a')]

        insert_data({
            'title': title,
            'text': text,
            'html': str(judgement_div),
            'reference': reference,
            'document_link': link,
            'search_url': full_url,
            'scraping_id': index,
            'scrapped_at': datetime.now().isoformat()
        })

        # data.append({
        #     'title':title,
        #     'text':text,
        #     'html':str(judgement_div),
        #     'reference':reference,
        #     'document_link':link,
        #     'search_url':full_url,
        #     'scrapped_at':datetime.now().isoformat()
        # })

    except Exception as e:
        # print(e)
        print("Error", item[0], "Waiting for 30 seconds")
        print('-------------------')

        if attempt > 3:
            print('Attempt limit reached:', attempt)
            return
        time.sleep(30)
        return get_judgement_data(item, index, attempt+1)


for index, item in enumerate(judgement_links):
    if len(threads) > 10:
        for t in threads:
            t.join()
        threads.clear()

        print("Completed -->",index+1,len(judgement_links))

    t = Thread(target=get_judgement_data, args=(item, index))
    t.start()

    threads.append(t)

for t in threads:
    t.join()


# print(len(data))

# import json
# with open('data/consumer_cases.json','w') as f:
#     json.dump(data,f,indent=4)


# df = pd.DataFrame(data)
# df.to_csv('data/consumer_cases.csv',index=False)
