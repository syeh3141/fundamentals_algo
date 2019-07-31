# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:51:36 2019

@author: syeh3
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
X, y = make_regression(n_samples = 1000, n_features=8, n_informative=3,
              random_state=0, shuffle=False)

X_train, X_test, y_train, y_test = train_test_split(
...     X, y, test_size=0.33)

regr = RandomForestRegressor(max_depth=2, random_state=0,
...                              n_estimators=100)
regr.fit(X_train,y_train)
regr.score(X_train,y_train)
regr.score(X_test,y_test)
regr.feature_importances_

EV
Trailing PE and Forward PE
PEG Ratio
Price/Sales and Price/Book
EV/R
EV/EBITDA

Profit Margin
Operating Margin
Current Ratio
Book Value Per Share
