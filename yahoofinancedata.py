# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 18:06:07 2019

@author: syeh3
"""

import urllib.request
from bs4 import BeautifulSoup
import json
import pandas as pd

pd.core.common.is_list_like = pd.api.types.is_list_like

from pandas_datareader.nasdaq_trader import get_nasdaq_symbols

def delTrailingNumber(name):
    """Deletes last number of a string
    returns new string or the old one if there was no trailing number"""
    if name[len(name)-1].isdigit():
        new_name = name[:len(name)-1].strip()
        return new_name
    else:
        return name

stocksList = []

symbols = get_nasdaq_symbols()

count = 0
while count < len(symbols):
    if 'Common Stock' in symbols.iloc[count].iloc[1]:
        stocksList.append(symbols.iloc[count].iloc[9])
    count += 1
print("Done getting NASDAQ stocks")
#with open('s_and_p_500_constituents_json.json') as json_file:
#    s_and_p_500_stocks = json.load(json_file)
    #Get list of S & P 500 Stocks
no_summary_stocks = []
stock_count = 0
for stock_symbol in stocksList:
    #STOCK_SYMBOL = s_and_p_500_stocks[count]['Symbol']
    STOCK_SYMBOL = stock_symbol
    print(STOCK_SYMBOL)

    all_stats = {}
    
    for i in range(0,10):
        try:    
            summary_url = "https://finance.yahoo.com/quote/" + STOCK_SYMBOL + "?p=" + STOCK_SYMBOL
            summary_url_headers = urllib.request.Request(summary_url, headers={'User-Agent' : "Magic Browser"})
            summary_html = urllib.request.urlopen(summary_url_headers)
            summary_soup = BeautifulSoup(summary_html, 'lxml')
        except:
            continue
        break

    try:
        summary_table = summary_soup.find("table", {"class": "W(100%) M(0) Bdcl(c)"})
        summary_table_rows = summary_table.find_all("tr")
        for row in summary_table_rows:
            stats = row.find_all("td")
            all_stats[stats[0].text] = stats[1].text
    except:
        print("No summary data")
        no_summary_stocks.append(STOCK_SYMBOL)
        continue
    
    for i in range(0,10):
        try:   
            key_stats_url = "https://finance.yahoo.com/quote/" + STOCK_SYMBOL + "/key-statistics?p=" + STOCK_SYMBOL
            key_stats_url_headers = urllib.request.Request(key_stats_url, headers={'User-Agent' : "Magic Browser"})
            key_html = urllib.request.urlopen(key_stats_url_headers)
            key_soup = BeautifulSoup(key_html, 'lxml')
        except:
            continue
        break

    key_all_tables = key_soup.find_all("table", {"class": "table-qsp-stats Mt(10px)"})
    for table in key_all_tables:
        table_rows = table.find_all("tr")
        for row in table_rows:
            stats = row.find_all("td")
            stat_name = delTrailingNumber(stats[0].text)
            all_stats[stat_name] = stats[1].text
            
    for i in range(0,10):
        try:   
            prof_stats_url = "https://finance.yahoo.com/quote/" + STOCK_SYMBOL + "/profile?p=" + STOCK_SYMBOL
            prof_stats_url_headers = urllib.request.Request(prof_stats_url, headers={'User-Agent' : "Magic Browser"})
            prof_html = urllib.request.urlopen(prof_stats_url_headers)
            prof_soup = BeautifulSoup(prof_html, 'lxml')
        except:
            continue
        break
    
    try:
        prof_p = prof_soup.find("p", {"class": "D(ib) Va(t)"})
        section_count = 0
        for section in prof_p.find_all("span", {"class": "Fw(600)"}):
            if section_count == 0:
                all_stats["Sector"] = section.text
            elif section_count == 1:
                all_stats["Industry"] = section.text
            elif section_count == 2:
                all_stats["Employees"] = section.text
            section_count += 1
    except:
        print("no profile info")
        pass
    
    for i in range(0,10):
        try:
            sust_stats_url = "https://finance.yahoo.com/quote/" + STOCK_SYMBOL + "/sustainability?p=" + STOCK_SYMBOL
            sust_stats_url_headers = urllib.request.Request(sust_stats_url, headers={'User-Agent' : "Magic Browser"})
            sust_html = urllib.request.urlopen(sust_stats_url_headers)
            sust_soup = BeautifulSoup(sust_html, 'lxml')
        except:
            continue
        break
    
    try:
        esg_data = sust_soup.find("div", {"class": "smartphone_Mt(20px)"})
        div_count = 0
        for div in esg_data:
            if div_count == 0:
                score_title = div.find("div", {"class": "C($c-fuji-grey-h) Fz(s)"}).text
                score = div.find("div", {"class": "Fz(36px) Fw(600) D(ib) Mend(5px)"}).text
                all_stats[score_title] = score
            else:
                score_title = div.find("div", {"class": "C($c-fuji-grey-h) Fz(s)"}).text
                score = div.find("div", {"class": "D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)"}).text
                all_stats[score_title] = score
            div_count += 1

        side_table = sust_soup.find("table", {"class": "W(100%)"})
        side_table_body = side_table.find("tbody")
        side_table_rows = side_table_body.find_all("tr")
        for row in side_table_rows:
            stats = row.find_all("td")
            all_stats[stats[0].text] = stats[1].text
    except:
        print("no sustainability info")
        pass
    
    with open('yahoofinance_stockdata/' + STOCK_SYMBOL + '.txt', 'w') as outfile:
            json.dump(all_stats, outfile)
    print(STOCK_SYMBOL + " success")
    stock_count += 1
    print(stock_count)

