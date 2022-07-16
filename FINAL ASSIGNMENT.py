#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[9]:


apple = yf.Ticker("AAPL")


# In[12]:


apple_data= apple.history(period='max')


# In[15]:


apple_data.reset_index(inplace=True)
apple_data.head()


# In[24]:


GameStop = yf.Ticker("GME")


# In[25]:


gme_data = GameStop.history(period='max')


# In[28]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[16]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
data  = requests.get(url).text


# In[17]:


soup = BeautifulSoup(data, 'html.parser')


# In[18]:


tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])


# In[19]:


for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text
    
    tesla_revenue = tesla_revenue.append({'Date':date, 'Revenue':revenue}, ignore_index=True)


# In[20]:


tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',|\$',"")


# In[21]:


tesla_revenue.dropna(inplace=True)


# In[22]:


tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[23]:


tesla_revenue.tail()


# In[29]:


url = " https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
data  = requests.get(url).text


# In[30]:


soup = BeautifulSoup(data, 'html.parser')


# In[31]:


gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])


# In[32]:


for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    revenue = col[1].text
    
    gme_revenue = gme_revenue.append({'Date':date, 'Revenue':revenue}, ignore_index=True)
    
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")  

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]    


# In[33]:


gme_revenue.tail()


# In[35]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[36]:


make_graph(apple_data, tesla_revenue, 'Tesla')


# In[37]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




