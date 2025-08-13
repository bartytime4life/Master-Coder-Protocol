from fastapi import FastAPI

from .predict import InputData, PredictionResult, predict

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/predict", response_model=PredictionResult)
def predict_endpoint(data: InputData) -> PredictionResult:
    return predict(data)
