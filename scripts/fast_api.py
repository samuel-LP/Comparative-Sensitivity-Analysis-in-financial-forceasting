import sys
sys.path.append("./scripts")
from fastapi import FastAPI
from pydantic import BaseModel
from main import *

class User_input(BaseModel):
    tickers:list
    model:str
    target :str
    horizon : int

app = FastAPI(debug = True)
@app.post("/prediction")
def operate(input: User_input):
    pred, ptf, error = forecast(User_input.tickers,User_input.model,User_input.target,User_input.horizon).run()
    return pred, ptf, error
