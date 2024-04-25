import yfinance as yf

from LSTM import PortfolioPredicitionsLSTM_value, PortfolioPredicitionsLSTM_volatility
from XGBoost import PortfolioPredictionXGBoost_value, PortfolioPredictionXGBoost_volatility
from LSTM_utils import *

class forecast():
    def __init__(self, tickers:list, model:str, target :str, horizon : int):
        self.tickers = tickers
        self.target = target
        self.model = model
        self.horizon = horizon

    def get_stocks(self):
        date_debut = "2013-01-02"
        date_fin = "2023-12-29"

        self.stocks_dic = {}

        for element in self.tickers:
            data = yf.download(element, start=date_debut, end=date_fin)
            data = data.reset_index()
            self.stocks_dic[element] = data

    def get_prediction(self):
        if self.model == 'LSTM':
            if self.target == 'Value':
                model = PortfolioPredicitionsLSTM_value(self.stocks_dic,
                                       n_steps = 30,
                                       epochs = 1,
                                       horizon_prev = self.horizon,
                                       test_size = 0.8)

            else :
                model = PortfolioPredicitionsLSTM_volatility(self.stocks_dic,
                                       n_steps = 30,
                                       epochs = 1,
                                       horizon_prev = self.horizon,
                                       test_size = 0.8)
        else :
            if self.target == 'Value':
                model = PortfolioPredictionXGBoost_value(self.stocks_dic,
                                       window_size = 30,
                                       horizon_prev = self.horizon,
                                       test_size = 0.8)

            else :
                model = PortfolioPredictionXGBoost_volatility(self.stocks_dic,
                                       window_size = 30,
                                       horizon_prev = self.horizon,
                                       test_size = 0.8)

        self.predictions, self.ptf_avg = model.predict_avg_portfolio()

    def get_metrics(self):
        if self.target == 'Value':
            self.errors = compute_errors(self.predictions, self.ptf_avg)
        else :
            self.errors = compute_errors_volatility(self.predictions, self.ptf_avg)

    def run(self):
        self.get_stocks()
        self.get_prediction()
        self.get_metrics()
        return(self.predictions, self.ptf_avg, self.errors)
