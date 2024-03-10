from fastapi import FastAPI
from pydantic import BaseModel
from main import forecast

class User_input(BaseModel):
    tickers:list
    model:str
    target :str
    horizon : int

app = FastAPI()
@app.post("/prediction")
def operate(input: User_input):
    stocks  = forecast.get_stocks()
    pred = forecast.get_prediction()
    metric = forecast.get_metrics()

    result = forecast.run()
    return result
