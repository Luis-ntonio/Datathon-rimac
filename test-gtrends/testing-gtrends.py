# connect to google 

from pytrends.request import TrendReq
import plotly.express as px
import pandas as pd
import sys
import json
from cities import cities
import time

def trends_by_region(title: str):
    #2 Interest by Region
    pytrends = TrendReq(hl='es-ES', tz=360)

    kw_list = [title] # list of keywords to get data 

    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='PE') 

    data_region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    data_region = data_region.reset_index()

    return data_region

def trends_related(title: str):
    #3 Related Queries
    pytrends = TrendReq(hl='es-ES', tz=360)

    kw_list = [title] # list of keywords to get data 

    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='PE') 

    data_related = pytrends.related_queries()
    data_related = data_related[title]['top']
    data_related = data_related.reset_index()

    return data_related

def trends_over_time(title: str, region: str):
    #1 Interest over Time
    pytrends = TrendReq(hl='es-ES', tz=360)

    kw_list = [title] # list of keywords to get data 

    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='PE-' + cities[region]) 

    data = pytrends.interest_over_time() 
    data = data.reset_index() # reset index

    return data

def get_trends(title: str):
    top_queries_per_region = {}
    pytrends = TrendReq(hl='es-ES', tz=360)

    related = trends_related(title)

    for index, row in related.iterrows():
        print(row['query'])
        region = trends_by_region(row['query'])
        region = region.sort_values(by=row['query'], ascending=False)
        for index, row_ in region.iterrows():
            if row_['geoName'] not in top_queries_per_region:
                top_queries_per_region[row_['geoName']] = [(row['query'], row_[row['query']])]
            else:
                top_queries_per_region[row_['geoName']].append((row['query'], row_[row['query']]))

    top_queries_per_region = sorted(top_queries_per_region.items(), key=lambda x: x[0])
    top_queries_per_region = dict(top_queries_per_region)
    with open(f'./data/dict_top.json', 'w') as file:
        json.dump(top_queries_per_region, file)
    

    top_queries_per_region = pd.DataFrame(top_queries_per_region)
    top_queries_per_region.to_csv(f'data/{title}_top_queries_per_region.csv', index=False, encoding='utf-8', header=True)

    #data.to_csv(f'data/{title}.csv', index=False, encoding='utf-8')

def historic_per_region(dict_path):
    with open(dict_path) as file:
        top_queries_per_region = json.load(file)

    for key, value in top_queries_per_region.items():
        for v in value:
            query = None
            for keys in top_queries_per_region.keys():
                print(keys, v[0])
                data = trends_over_time(v[0], keys)
                time.sleep(1)
                if query is None:
                    query = pd.DataFrame(data)
                    query = query.rename({v[0]: f"{v[0]}-{keys}"}, axis=1)
                else:
                    query[f"{v[0]}-{keys}"] = data[v[0]] if v[0] in data.columns else 0
            query.to_csv(f'data/{v[0]}.csv', index=False, encoding='utf-8')
        break


if __name__ == '__main__':
    title = sys.argv[1]
    #get_trends(title)
    #print(trends_by_region("seguro de salud"))
    historic_per_region('./data/dict_top.json')