# connect to google 

from pytrends.request import TrendReq
import plotly.express as px
import pandas as pd
import sys
import json
from cities import cities

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

    pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='PE-' + cities[region]) 

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
    with open(f'dict_top.json', 'w') as file:
        json.dump(top_queries_per_region, file)
    """for key, value in top_queries_per_region.items():
        query = {}
        for v in value:
            for keys in top_queries_per_region.keys():
                data = trends_over_time(v, key)
            if v in query:
                query[v] = [data['value']]
            else:
                query[v].append([data['value']])
        with open(f'{v}.json', 'w') as file:
            json.dump(query, file)"""
    

    top_queries_per_region = pd.DataFrame(top_queries_per_region)
    top_queries_per_region.to_csv(f'data/{title}_top_queries_per_region.csv', index=False, encoding='utf-8', header=True)

    #data.to_csv(f'data/{title}.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    title = sys.argv[1]
    get_trends(title)
    #print(trends_by_region("seguro de salud"))