from pydantic import BaseModel


class InputData(BaseModel):
    feature: float


class PredictionResult(BaseModel):
    prediction: float
    confidence: float


def predict(data: InputData) -> PredictionResult:
    # Simple heuristic
    pred = data.feature * 0.5
    return PredictionResult(prediction=pred, confidence=0.8)
