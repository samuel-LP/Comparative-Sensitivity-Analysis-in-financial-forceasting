import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def prepare_data_value(stock, horizon_prev, test_size, window_size):
    stock_copy = stock.copy()

    split = int(test_size * stock_copy.shape[0])
    stock_copy = stock_copy.iloc[split - window_size:].copy()

    stock_copy['Date'] = pd.to_datetime(stock_copy['Date'])
    stock_copy.drop(columns=["Volume"], inplace=True)

    stock_copy["Target"] = stock_copy["Close"].shift(-horizon_prev)
    stock_copy.dropna(inplace=True)

    return stock_copy


def prepare_data_volatility(stock, horizon_prev, test_size, window_size):
    stock_copy = stock.copy()

    split = int(test_size * stock_copy.shape[0])
    stock_copy = stock_copy.iloc[split - window_size:].copy()
    stock_copy['Date'] = pd.to_datetime(stock_copy['Date'])

    stock_copy.drop(columns=["Volume"], inplace=True)

    stock_copy["ret"] = stock_copy['Close'].pct_change()
    stock_copy.dropna(inplace=True)

    stock_copy["Volatility"] = stock_copy['ret'].rolling(window=10).std()
    stock_copy.dropna(inplace=True)

    stock_copy["Target"] = stock_copy["Volatility"].shift(-horizon_prev)
    stock_copy.dropna(inplace=True)

    return stock_copy