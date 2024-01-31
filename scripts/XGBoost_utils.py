import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def data_preparation_portfolio(stock: pd.DataFrame) -> pd.DataFrame:

    """
    Will change the format of the "Date" column and
    create the new features in the dataframe.

    Parameters
    ----------
    stock : pd.DataFrame
        The stock dataframe

    Returns
    -------
    pd.DataFrame
        The stock dataframe with the new features

    """

    stock['Date'] = pd.to_datetime(stock['Date'])
    # stock = stock[stock["Date"]>="2020-07-01"]
    stock['Adj Close'] = stock['Adj Close'].pct_change()
    stock['High'] = stock['High'].pct_change()
    stock['Low'] = stock['Low'].pct_change()
    stock['Volume'] = stock['Volume'].pct_change()
    stock['dailyChange'] = (stock['Adj Close'] - stock['Open']) / stock['Open']

    stock['VolMA10'] = stock['Volume'].rolling(window=10).mean()

    stock['priceDirection'] = stock['Adj Close'].shift(-1) - stock['Adj Close']

    stock['Std_dev'] = stock['Adj Close'].rolling(10).std()

    stock['Williams%R'] = \
        (stock['High'].max() - stock['Adj Close'])/(stock['High'] - stock['Low'].min()) * -100
    stock = stock.replace([np.inf, -np.inf], np.nan)

    stock['Volatility_HighLow_10days'] = \
        stock['High'].rolling(window=10).std() / stock['Low'].rolling(window=10).mean()

    stock['Return'] = stock['Close'].pct_change()
    stock = stock.dropna()
    stock = stock.drop(columns=['Adj Close'])

    stock['Target'] = stock['Return'].shift(-10)
    stock = stock.dropna()

    return stock


def data_preparation_volatility(stock: pd.DataFrame) -> pd.DataFrame:

    """
    Will change the format of the "Date" column and
    create the new features in the dataframe.

    Parameters
    ----------
    stock : pd.DataFrame
        The stock dataframe

    Returns
    -------
    pd.DataFrame
        The stock dataframe with the new features

    """

    stock['Date'] = pd.to_datetime(stock['Date'])

    stock['Return'] = stock['Close'].pct_change()

    # Calcul de la volatilité sur une fenêtre mobile
    stock['Volatility'] = stock['Return'].rolling(window=10).std()

    # Définition de la cible comme la volatilité future
    stock['Target'] = stock['Volatility'].shift(-10)
    stock['Date'] = pd.to_datetime(stock['Date'])
    stock['Adj Close'] = stock['Adj Close'].pct_change()
    stock['High'] = stock['High'].pct_change()
    stock['Low'] = stock['Low'].pct_change()
    stock['Volume'] = stock['Volume'].pct_change()
    stock['dailyChange'] = (stock['Adj Close'] - stock['Open']) / stock['Open']

    stock['VolMA10'] = stock['Volume'].rolling(window=10).mean()

    stock['priceDirection'] = (stock['Adj Close'].shift(-1) - stock['Adj Close'])

    stock['Std_dev'] = stock['Adj Close'].rolling(10).std()

    stock['Williams%R'] = (stock['High'].max() - stock['Adj Close'])/(stock['High'] - stock['Low'].min()) * -100
    stock = stock.replace([np.inf, -np.inf], np.nan)
    stock = stock.drop(columns=["Open", 'Adj Close'])

    stock.dropna(inplace=True)
    return stock

def compute_errors(dict_df, ptf):

    """
    Compute errors for the given portfolio and dataframes.

    Parameters:
    - dict_df: a dictionary of dataframes containing the stock data
    - ptf: a dataframe representing the portfolio

    Returns:
    - resultats: a dataframe containing the computed errors for the
    portfolio and stocks
    """

    resultats = pd.DataFrame(columns=['MSE', 'RMSE', 'MAE'])

    mse_ptf = mean_squared_error(ptf["Predicted_Portfolio_Value"],
                                 ptf["Real_Portfolio_Value"])
    mae_ptf = mean_absolute_error(ptf["Predicted_Portfolio_Value"],
                                  ptf["Real_Portfolio_Value"])
    rmse_ptf = np.sqrt(mse_ptf)

    resultats.loc["Portfolio"] = [mse_ptf, rmse_ptf, mae_ptf]

    for actif, df in dict_df.items():
        mse = mean_squared_error(df['Close'], df['Prediction'])
        mae = mean_absolute_error(df['Close'], df['Prediction'])
        rmse = np.sqrt(mse)

        resultats.loc[actif] = [mse, rmse, mae]
    return resultats


def compute_errors_volatility(dict_df, ptf):
    """
    Compute errors (MSE, RMSE, MAE) for a portfolio and individual assets
    given a dictionary of dataframes and a portfolio dataframe.

    Parameters:
    - dict_df: a dictionary of dataframes where the keys are asset names and
    the values are dataframes containing 'Volatility' and 'Prediction' columns.

    - ptf: a dataframe containing 'Volatility' and 'Prediction'
    columns for the portfolio.

    Returns:
    - resultats: a dataframe containing the MSE, RMSE, and MAE for the
    portfolio and each individual asset.
    """
    resultats = pd.DataFrame(columns=['MSE', 'RMSE', 'MAE'])

    mse_ptf = mean_squared_error(ptf["Prediction"], ptf["Volatility"])
    mae_ptf = mean_absolute_error(ptf["Prediction"], ptf["Volatility"])
    rmse_ptf = np.sqrt(mse_ptf)

    resultats.loc["Portfolio"] = [mse_ptf, rmse_ptf, mae_ptf]

    for actif, df in dict_df.items():
        mse = mean_squared_error(df['Volatility'], df['Prediction'])
        mae = mean_absolute_error(df['Volatility'], df['Prediction'])
        rmse = np.sqrt(mse)

        resultats.loc[actif] = [mse, rmse, mae]

    return resultats
