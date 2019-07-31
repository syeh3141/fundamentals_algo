# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:24:43 2019

@author: syeh3
"""

import numpy as np
import matplotlib.pyplot as plt
import json

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

pd.core.common.is_list_like = pd.api.types.is_list_like

from pandas_datareader.nasdaq_trader import get_nasdaq_symbols

stocksList = []

symbols = get_nasdaq_symbols()

count = 0
while count < len(symbols):
    if 'Common Stock' in symbols.iloc[count].iloc[1]:
        stocksList.append(symbols.iloc[count].iloc[9])
    count += 1
print("Done getting NASDAQ stocks")

consumer_cyclical = []

for stock_symbol in stocksList:
    STOCK_SYMBOL = stock_symbol
    try:
        with open("yahoofinance_stockdata/" + STOCK_SYMBOL + ".txt") as json_file:  
            data = json.load(json_file)
    except FileNotFoundError:
        continue
    if "Sector" in data and data["Sector"] == "Consumer Cyclical":
        consumer_cyclical.append(STOCK_SYMBOL)

#to change for new x-axis
x_variable = []
price_change = []
not_enough_data = []

for stock_symbol in consumer_cyclical:
    print(stock_symbol)
    try:
        with open('consumer_cyclicals/' + stock_symbol +'.txt') as json_file:
            price_data = json.load(json_file)
    
        two_months_open = float(price_data["history"]["2019-05-15"]["open"])
        close = float(price_data["history"]["2019-07-15"]["close"])
        price_change.append(((close - two_months_open)/two_months_open)*100)

        with open('yahoofinance_stockdata/' + stock_symbol + '.txt') as json_file:  
            financial_data = json.load(json_file)
            
        #to change for new x-axis
        x_variable.append(float(financial_data["Quarterly Revenue Growth (yoy)"].replace('%','')))
        print(float(financial_data["Quarterly Revenue Growth (yoy)"].replace('%','')))
    except:
        print("not enough data for " + stock_symbol)
        not_enough_data.append(stock_symbol)
        continue

for stock in not_enough_data:
    consumer_cyclical.remove(stock)


trace = go.Scatter(
    #to change for new x-axis
    x = x_variable,
    y = price_change,
    mode = 'markers',
    text = consumer_cyclical
)

data = [trace]
#to change for new x-axis
#py.iplot(data, filename='pe-ratio-scatter')
