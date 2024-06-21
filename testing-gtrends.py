# connect to google 

from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='es-ES', tz=360)

# build payload

kw_list = ["seguro"] # list of keywords to get data 

pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='PE') 

#1 Interest over Time
data = pytrends.interest_over_time() 
data = data.reset_index() 

data.to_csv('data.csv', index=False, encoding='utf-8')

import plotly.express as px

fig = px.line(data, x="date", y=['seguro'], title='Keyword Web Search Interest Over Time')
fig.show() 