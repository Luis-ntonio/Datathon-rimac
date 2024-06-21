# connect to google 

from pytrends.request import TrendReq
import plotly.express as px
import pandas as pd
import sys

def get_trends(title: str):
    pytrends = TrendReq(hl='es-ES', tz=360)

    # build payload



    kw_list = [title] # list of keywords to get data 

    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='PE') 

    #1 Interest over Time
    data = pytrends.interest_over_time() 
    data = data.reset_index() 


    fig = px.line(data, x="date", y=[title], title='Keyword Web Search Interest Over Time')
    fig.show() 

    data.to_csv(f'{title}.csv', index=False, encoding='utf-8')

    by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)

    by_region.head(10) 

if __name__ == '__main__':
    try:
        title = sys.argv[1]
        get_trends(title)
    except Exception as e:
        print(e)
        print('Usage: python testing-gtrends.py <title>')