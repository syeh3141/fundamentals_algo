# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:27:14 2019

@author: syeh3
"""

from sklearn.linear_model import Ridge
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt
import numpy as np
import json
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


price_change = []
missing_price_stocks = []
no_file = []
for stock_symbol in consumer_cyclical:
    print(stock_symbol)
    try:
        with open('consumer_cyclicals/' + stock_symbol +'.txt') as json_file:
            price_data = json.load(json_file)
    
        two_months_open = float(price_data["history"]["2019-05-15"]["open"])
        close = float(price_data["history"]["2019-07-15"]["close"])
        price_change.append(((close - two_months_open)/two_months_open)*100)
    except KeyError:
        print("no two month data")
        missing_price_stocks.append(stock_symbol)
        continue
    except FileNotFoundError:
        print("no file")
        no_file.append(stock_symbol)
        continue
    
for stock_symbol in no_file + missing_price_stocks:
    consumer_cyclical.remove(stock_symbol)
    
"""stats = ["PE Ratio (TTM)","EPS (TTM)","Trailing P/E ","Forward P/E","PEG Ratio (5 yr expected)",
         "Price/Sales (ttm)","Price/Book (mrq)","Enterprise Value/Revenue",
         "Enterprise Value/EBITDA","Profit Margin ","Operating Margin (ttm)",
         "Return on Assets (ttm)","Return on Equity (ttm)","Revenue Per Share (ttm)",
         "Quarterly Revenue Growth (yoy)","Quarterly Earnings Growth (yoy)",
         "Total Debt/Equity (mrq)", "Current Ratio (mrq)", "Book Value Per Share (mrq)"]"""

stats = ["EPS (TTM)","PEG Ratio (5 yr expected)","Price/Sales (ttm)","Price/Book (mrq)",
         "Enterprise Value/Revenue","Enterprise Value/EBITDA","Profit Margin ","Operating Margin (ttm)",
         "Return on Assets (ttm)","Return on Equity (ttm)","Revenue Per Share (ttm)",
         "Quarterly Revenue Growth (yoy)","Total Debt/Equity (mrq)", "Current Ratio (mrq)", "Book Value Per Share (mrq)"]


per_stat_missing = {}
for stat in stats:
    per_stat_missing[stat] = 0
    
all_financial_data = []
for stock_symbol in consumer_cyclical:
    print(stock_symbol)
    with open('yahoofinance_stockdata/' + stock_symbol + '.txt') as json_file:  
            financial_data = json.load(json_file)
    one_stock_financial_data = []
    for stat in stats:
        if stat in financial_data:
            one_stock_financial_data.append(financial_data[stat].replace("%","").replace(",",""))
            if financial_data[stat] == "N/A":
                per_stat_missing[stat] += 1
        else:
            one_stock_financial_data.append("N/A")
            per_stat_missing[stat] += 1
    all_financial_data.append(one_stock_financial_data) 

count_above = 0
missing_financial_stats = []
for stock in all_financial_data:
    count_missing = 0
    for number in stock:
        if number == "N/A":
            count_missing += 1
    missing_financial_stats.append(count_missing)
    if count_missing >=4:
        count_above += 1
    
with_names = {}
count = 0
for stock in consumer_cyclical:
    with_names[stock] = missing_financial_stats[count]
    count+=1
    
    
converted_data = []
    
for stock in all_financial_data:
    new_list = []
    for num in stock:
        if num == "N/A":
            new_list.append(np.nan)
        else:
            new_list.append(num)
    converted_data.append(new_list)

imputer = Imputer(missing_values=np.nan , strategy = "mean", axis = 0)
converted_data = imputer.fit_transform(converted_data)


# Ridge trace plot
n_alphas = 1000
alphas = np.logspace(-10, 10, n_alphas)

r_squares = []
coefs = []
for a in alphas:
    ridge = Ridge(alpha=a, fit_intercept=False)
    ridge.fit(converted_data, price_change)
    coefs.append(ridge.coef_)
    r_squares.append(ridge.score(converted_data, price_change))

# Display results

plt.subplot(121)
ax = plt.gca()

ax.plot(alphas, coefs)
ax.set_xscale('log')
ax.set_xlim(ax.get_xlim()[::-1])  # reverse axis
plt.xlabel('alpha')
plt.ylabel('weights')
plt.title('Ridge coefficients as a function of the regularization')
plt.axis('tight')


plt.subplot(122)
ax = plt.gca()

ax.plot(alphas, r_squares)
ax.set_xscale('log')
ax.set_xlim(ax.get_xlim()[::-1])  # reverse axis
plt.xlabel('alpha')
plt.ylabel('R_squared')
plt.title('R-squared as a function of the regularization')
plt.axis('tight')
plt.show()



