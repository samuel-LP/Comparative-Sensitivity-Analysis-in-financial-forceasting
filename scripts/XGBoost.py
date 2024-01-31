import pandas as pd
from XGBoost_utils import prepare_data_value, prepare_data_volatility
from tqdm import tqdm
from xgboost import XGBRegressor

class PortfolioPredictionXGBoost_value():
    def __init__(self, stock_dict, window_size, test_size, horizon_prev):
        self.stock_dict = stock_dict
        self.window_size = window_size
        self.test_size = test_size
        self.horizon_prev = horizon_prev

    def XG_boost_rolling_window(self, stock: pd.DataFrame):

        stock = prepare_data_value(stock, self.horizon_prev, self.test_size, self.window_size)
        prediction_dates = []
        predictions = []

        features_to_drop = ['Date', 'Target']
        for start in range(0, len(stock) - self.window_size - self.horizon_prev):
            end = start + self.window_size
            train = stock[start:end].copy()
            test = stock[end:end + self.horizon_prev].copy()

            model = XGBRegressor(n_estimators=400,
                                 max_depth=30,
                                 learning_rate=0.01,
                                 verbosity=0)

            model.fit(train.drop(features_to_drop, axis=1), train['Target'])

            pred = model.predict(test.drop(['Date', 'Target'], axis=1))
            predictions.append(pred)

            prediction_date = stock.iloc[end + self.horizon_prev - 1]['Date']

            prediction_dates.append(prediction_date)

        predictions = [value[self.horizon_prev - 1] for value in predictions]

        df_predictions = pd.DataFrame({'Date': prediction_dates,
                                       'Prediction': predictions})

        predicted_df = stock.merge(df_predictions, on='Date', how='inner')

        return predicted_df

    def compute_stock_returns(self, predicted_df):

        predicted_df = predicted_df.drop(columns=["Target", "Adj Close", "High", "Low", "Open"])

        predicted_df['Real_Return'] = predicted_df['Close'].pct_change()
        predicted_df['Predicted_Return'] = predicted_df['Prediction'].pct_change()

        predicted_df = predicted_df.dropna()

        return (predicted_df)

    def predict_portfolio(self):
        self.predictions_dic = {}

        for key in tqdm(self.stock_dict):
            self.predictions_dic[key] = self.XG_boost_rolling_window(self.stock_dict[key])
            self.predictions_dic[key] = self.compute_stock_returns(self.predictions_dic[key])

    def compute_portfolio(self):
        dfs_to_concat = []

        for name, df in self.predictions_dic.items():
            df['Date'] = pd.to_datetime(df['Date'])
            dfs_to_concat.append(df[['Date', 'Real_Return', 'Predicted_Return']])

        portfolio_predictions = pd.concat(dfs_to_concat)

        self.portfolio_avg_predictions = \
            portfolio_predictions.groupby('Date').mean().reset_index()

        self.portfolio_avg_predictions['Real_Portfolio_Value'] = \
            1000 * (1 + self.portfolio_avg_predictions['Real_Return']).cumprod()
        self.portfolio_avg_predictions['Predicted_Portfolio_Value'] = \
            1000 * (1 + self.portfolio_avg_predictions['Predicted_Return']).cumprod()

    def predict_avg_portfolio(self):

        self.predict_portfolio()
        self.compute_portfolio()

        return self.predictions_dic, self.portfolio_avg_predictions


class PortfolioPredictionXGBoost_volatility():
    def __init__(self, stock_dict, window_size, test_size, horizon_prev):
        self.stock_dict = stock_dict
        self.window_size = window_size
        self.test_size = test_size
        self.horizon_prev = horizon_prev

    def XG_boost_rolling_window(self, stock: pd.DataFrame):

        stock = prepare_data_volatility(stock, self.horizon_prev, self.test_size, self.window_size)
        prediction_dates = []
        predictions = []

        features_to_drop = ['Date', 'Target']
        for start in range(0, len(stock) - self.window_size - self.horizon_prev):
            end = start + self.window_size
            train = stock[start:end].copy()
            test = stock[end:end + self.horizon_prev].copy()

            model = XGBRegressor(n_estimators=400,
                                 max_depth=30,
                                 learning_rate=0.01,
                                 verbosity=0)

            model.fit(train.drop(features_to_drop, axis=1), train['Target'])

            pred = model.predict(test.drop(['Date', 'Target'], axis=1))
            predictions.append(pred)

            prediction_date = stock.iloc[end + self.horizon_prev - 1]['Date']

            prediction_dates.append(prediction_date)

        predictions = [value[self.horizon_prev - 1] for value in predictions]

        df_predictions = pd.DataFrame({'Date': prediction_dates,
                                       'Prediction': predictions})

        predicted_df = stock.merge(df_predictions, on='Date', how='inner')

        return predicted_df

    def predict_portfolio(self):
        self.predictions_dic = {}

        for key in tqdm(self.stock_dict):
            self.predictions_dic[key] = self.XG_boost_rolling_window(self.stock_dict[key])

    def compute_portfolio(self):
        dfs_to_concat = []

        for name, df in self.predictions_dic.items():
            df['Date'] = pd.to_datetime(df['Date'])

            dfs_to_concat.append(df[['Date', 'Prediction', 'Volatility']])

        portfolio_predictions = pd.concat(dfs_to_concat)

        self.portfolio_avg_predictions = portfolio_predictions.groupby('Date').mean().reset_index()

    def predict_avg_portfolio(self):

        self.predict_portfolio()
        self.compute_portfolio()

        return self.predictions_dic, self.portfolio_avg_predictions