# Comparative Sensitivity Analysis of LSTM and XGBoost in Financial Forecasting 📈

Welcome to the repository for the project on "Comparative Sensitivity Analysis of LSTM and XGBoost in Financial Forecasting". This repository holds the complete codebase used to conduct the analysis presented in the associated paper.

## Abstract of the Paper
The paper undertakes a sensitivity analysis of two cutting-edge Machine Learning models - Long Short-Term Memory (LSTM) and Extreme Gradient Boosting (XGBoost) - in the context of financial forecasting. The aim is to evaluate the performance of these models in predicting stock closing prices and market volatility, with particular attention to the forecast horizon and the division of data into training and testing sets. An equiweighted portfolio comprising five S&P 500 stocks forms the basis of our analysis. We methodically investigate how changing forecast horizons and training/testing data splits affect the precision and robustness of LSTM and XGBoost models in price forecasting and volatility estimation. The results provide valuable insights into the models' adaptability and efficiency when applied to financial data, highlighting the crucial roles of model tuning and data structuring in enhancing forecast accuracy. This research serves as a useful resource for financial practitioners who aim to leverage these models for more precise market predictions.

## Repository Structure
The repository is structured into several folders, each containing Jupyter notebooks and Python scripts that correspond to different aspects of the analysis:

- **Forecast_horizon**: Contains Jupyter notebooks for the sensitivity analysis on the forecast horizon both for LSTM and XGBoost models. 
Each filenames indicates the forecast horizon (e.g., LSTM_Value_7.ipynb corresponds to an LSTM model predicting 7 days ahead).
- **Time_split**: Contains Jupyter notebooks for the sensitivity analysis of the time split both for LSTM and XGBoost models. 
Each filenames indicates the split used (e.g., LSTM_Value_80_20.ipynb corresponds to an LSTM model with a 80%/20% train test split).
- **Scripts**: Includes Python scripts with the core functions and utilities used by the Jupyter notebooks. LSTM.py and XGBoost.py contain the model definitions, while LSTM_utils.py and XGBoost_utils.py include helper functions for data preprocessing, feature extraction, and other necessary operations.

## To replicate the findings or conduct your own analysis:

1. Clone the repository

    ```bash
    git clone https://github.com/samuel-LP/finance_quant.git
    ```

2. Create a virtual environnement

   2.1 For windows users : 
   
   ```bash
    python -m venv venv
    .\venv\Scripts\activate
   ```
   
   2.2  For Mac users : 

   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

3. Install the dependencies : 
   ```bash
    pip install -r requirements.txt
   ```

## Authors

- [Samuel Baheux](https://github.com/SamuelBaheux)
- [Samuel Launay Pariente](https://github.com/samuel-LP)
- [Axel Fritz](https://github.com/AxelFritz1)