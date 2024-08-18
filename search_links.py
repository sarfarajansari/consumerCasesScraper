# /search/?formInput=doctypes:consumer fromdate:1-1-1800 todate: 31-12-1800

import pandas as pd
from datetime import datetime,timedelta

def first_date_of_year(year_str):
    year = int(year_str)  # Convert the year string to an integer
    return datetime(year, 1, 1)

def last_date_of_year(year_str):
    year = int(year_str)  # Convert the year string to an integer
    return datetime(year, 12, 31)



data = []
def generate_search_link(year,days=4):
    start = first_date_of_year(year)
    end = last_date_of_year(year)
    
    delta = timedelta(days=days)

    while start < end:
        next_date = start + delta
        if next_date > end:
            next_date = end
        search_link = f'/search/?formInput=doctypes:consumer fromdate:{start.strftime("%d-%m-%Y")} todate:{next_date.strftime("%d-%m-%Y")}'
        data.append((len(data)+1,search_link))
        start = next_date

    


    

    


years_data = pd.read_csv('data/year_data.csv').values.tolist()



for year,count in years_data:
    margin_count = 3 * count
    count_per_day = margin_count / 365
    days_for_400 = 400 / count_per_day
    generate_search_link(year,days_for_400)

    print(year,count,days_for_400,count_per_day)
    


print(len(data))
df = pd.DataFrame(data,columns=['search_id','search_link'])
df.to_csv('data/searchlinks.csv',index=False)