import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

def time_split(df, test_size):
    split = int(len(df) * test_size)
    train = df[:split]
    test = df[split:]

    return (train, test, split)

def prepare_data(data, n_steps, n_future=1):
    x, y = [], []

    if n_future == 1 :
        for i in range(len(data) - n_steps):
            x.append(data[i:(i + n_steps), 0])
            y.append(data[i + n_steps, 0])
        return np.array(x), np.array(y)
    else :
        for i in range(len(data) - n_steps - n_future + 1):
            x.append(data[i:(i + n_steps), 0])
            y.append(data[(i + n_steps):(i + n_steps + n_future), 0])
        return np.array(x), np.array(y)


def compute_errors(dict_df, ptf):
    resultats = pd.DataFrame(columns=['MSE', 'RMSE', 'MAE'])

    mse_ptf = mean_squared_error(ptf["Predicted_Portfolio_Value"], ptf["Real_Portfolio_Value"])
    mae_ptf = mean_absolute_error(ptf["Predicted_Portfolio_Value"], ptf["Real_Portfolio_Value"])
    rmse_ptf = np.sqrt(mse_ptf)

    resultats.loc["Portfolio"] = [mse_ptf, rmse_ptf, mae_ptf]

    for actif, df in dict_df.items():
        mse = mean_squared_error(df['Close'], df['Prediction'])
        mae = mean_absolute_error(df['Close'], df['Prediction'])
        rmse = np.sqrt(mse)

        resultats.loc[actif] = [mse, rmse, mae]

    resultats = resultats.reset_index()
    return resultats

def compute_errors_volatility(dict_df, ptf):
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

    resultats = resultats.reset_index()
    return resultats