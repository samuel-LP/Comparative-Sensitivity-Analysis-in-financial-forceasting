from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from scripts.main import forecast

app = FastAPI()


class PredictionRequest(BaseModel):
    tickers: List[str]
    model: str
    target: str
    horizon: int


@app.post("/predict/")
def get_prediction(request: PredictionRequest):
    prediction_model = forecast(tickers=request.tickers,
                                model=request.model,
                                target=request.target,
                                horizon=request.horizon)
    prediction_model.run()
    return {
            "predictions": prediction_model.predictions,
            "portfolio_average": prediction_model.ptf_avg,
            "errors": prediction_model.errors
        }
