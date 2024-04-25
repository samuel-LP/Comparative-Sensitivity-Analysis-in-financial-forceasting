# Financial forecasting application with LSTM and XGBoost 📈

## Presentation

Welcome on our application for financial forecasting ! \
The aims of the application is to predict the evolution of a financial asset among the time.

You can choose multiple options here :
- The asset : you can choose one of the pre-load asset datas, or choose one directly on the application.
- the target : do you want to predict the price or the volatility of the asset ?
- the model : do you want a deep learning model (with LSTM) or a machine learning model (with XGBoost) ?
- the horizon of prediction : 1 day, 7 days, 14 days or 28 days ?

This application is developped in streamlit and use fast API.

Enjoy!
## Repository Structure
The repository is structured into several folders, each containing Jupyter notebooks and Python scripts that correspond to different aspects of the analysis:
- **notebooks** : 
  - **Forecast_horizon**: Contains Jupyter notebooks for the sensitivity analysis on the forecast horizon both for LSTM and XGBoost models. 
  Each filenames indicates the forecast horizon (e.g., LSTM_Value_7.ipynb corresponds to an LSTM model predicting 7 days ahead).
  - **Time_split**: Contains Jupyter notebooks for the sensitivity analysis of the time split both for LSTM and XGBoost models. 
  Each filenames indicates the split used (e.g., LSTM_Value_80_20.ipynb corresponds to an LSTM model with a 80%/20% train test split).
- **Scripts**: Includes Python scripts with the core functions and utilities used by the Jupyter notebooks. LSTM.py and XGBoost.py contain the model definitions, while LSTM_utils.py and XGBoost_utils.py include helper functions for data preprocessing, feature extraction, and other necessary operations. This folder also contains the script needed to run the streamlit app.

## To run the Streamlit App and the FastAPI 

To run the streamlit app, you need to start the fastAPI server et the streamlit app itself : 
    
```bash
uvicorn scripts.fast_api:app --reload

streamlit run ./scripts/app.py      
```

If you wants to get results without running the app, you can start the FastAPI server and then make a post command to send this type of json : 

```bash
{
  "tickers":["AMZN"],
  "model":"LSTM",
  "target" :"Value",
  "horizon" : 7
}

```

## To replicate the findings or conduct your own analysis:

1. Clone the repository

    ```bash
    git clone git@github.com:samuel-LP/financial-forecasting-app.git
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
