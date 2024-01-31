import pandas as pd
from XGBoost_utils import data_preparation_portfolio, data_preparation_volatility
from tqdm import tqdm
from xgboost import XGBRegressor

class PortfolioPredictionXGBoost_value():

    def __init__(self, stock_dict, window_size, step_size, prediction_days):
        self.stock_dict = stock_dict
        self.window_size = window_size
        self.step_size = step_size
        self.prediction_days = prediction_days

    def xgboost_value(self, stock: pd.DataFrame, window_size_value: int,
                      step_size_value: int, prediction_days_value: int):
        
        stock = data_preparation_portfolio(stock)

        self.window_size = window_size_value
        self.step_size = step_size_value
        self.prediction_days = prediction_days_value

        prediction_dates = []
        predictions = []
  
        features_to_drop = ['Date', 'Target', 'Volume']
        for start in tqdm(range(0, len(stock) - self.window_size - self.prediction_days, self.step_size)):

            end = start + self.window_size
            train = stock.iloc[start:end]
            test = stock.iloc[end:end + self.prediction_days]
        
            model = XGBRegressor(n_estimators=400, max_depth=30,
                                 learning_rate=0.01, verbosity=0)

            model.fit(train.drop(features_to_drop, axis=1), train['Target'])

            pred = model.predict(test.drop(['Date', 'Target', 'Volume'], axis=1))
            predictions.append(pred)
        
            prediction_date = stock.iloc[end + self.prediction_days - 1]['Date']

            prediction_dates.append(prediction_date)

        predictions = [value[6] for value in predictions]

        df_predictions = pd.DataFrame({
            'Date': prediction_date,
            'Prediction': predictions
        })
        merged_df = stock.merge(df_predictions, on='Date', how='inner')
        merged_df = merged_df.drop(columns=["Target"])
        return merged_df

    def predict_portfolio(self):

        self.predictions_dic = {}

        for key in tqdm(self.stock_dict):
            self.predictions_dic[key] = \
                self.xgboost_value(self.stock_dict[key], self.window_size,
                                   self.step_size, self.prediction_days)

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

    def __init__(self, stock_dict, window_size, step_size, prediction_days):
        self.stock_dict = stock_dict
        self.window_size = window_size
        self.step_size = step_size
        self.prediction_days = prediction_days

        
    def xgboost_value(self, stock: pd.DataFrame, window_size_value: int,
                        step_size_value: int, prediction_days_value: int):

            stock = data_preparation_volatility(stock)

            self.window_size = window_size_value
            self.step_size = step_size_value
            self.prediction_days = prediction_days_value

            prediction_dates = []
            predictions = []
    
            features_to_drop = ['Date', 'Target', 'Volume']
            for start in tqdm(range(0, len(stock) - self.window_size - self.prediction_days, self.step_size)):

                end = start + self.window_size
                train = stock.iloc[start:end]
                test = stock.iloc[end:end + self.prediction_days]
            
                model = XGBRegressor(n_estimators=400, max_depth=30,
                                    learning_rate=0.01, verbosity=0)

                model.fit(train.drop(features_to_drop, axis=1), train['Target'])

                pred = model.predict(test.drop(['Date', 'Target', 'Volume'], axis=1))
                predictions.append(pred)
            
                prediction_date = stock.iloc[end + self.prediction_days - 1]['Date']

                prediction_dates.append(prediction_date)

            predictions = [value[6] for value in predictions]

            df_predictions = pd.DataFrame({
                'Date': prediction_date,
                'Prediction': predictions
            })
            merged_df = stock.merge(df_predictions, on='Date', how='inner')
            merged_df = merged_df.drop(columns=["Target"])
            return merged_df

    def predict_portfolio(self):

        self.predictions_dic = {}

        for key in tqdm(self.stock_dict):
            self.predictions_dic[key] = \
                self.xgboost_value(self.stock_dict[key], self.window_size,
                                   self.step_size, self.prediction_days)
    
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
