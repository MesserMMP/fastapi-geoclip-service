from pydantic import BaseModel
from typing import List


class Prediction(BaseModel):
    lat: float
    lon: float
    prob: float


class PredictResponse(BaseModel):
    predictions: List[Prediction]


class Match(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    url: str
    distance_km: float


class NearbyResponse(BaseModel):
    center: dict[str, float]
    matches: List[Match]
