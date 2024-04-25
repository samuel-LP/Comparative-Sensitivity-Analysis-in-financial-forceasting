import sys
sys.path.append("./scripts")
from fastapi import FastAPI
from pydantic import BaseModel
from main import *


class User_input(BaseModel):

    tickers : list
    model : str
    target : str
    horizon : int


app = FastAPI(debug=True)
@app.post("/prediction")
def operate(input:User_input):
    model = forecast(input.tickers,
                     input.model,
                     input.target,
                     input.horizon)

    pred, ptf, error = model.run()

    pred_json = {key: value.to_json(orient="records") for key, value in pred.items()}

    ptf_json = ptf.to_json(orient="records")
    error_json = error.to_json(orient="records")

    return {"predictions": pred_json,
            "portfolio": ptf_json,
            "error": error_json}
