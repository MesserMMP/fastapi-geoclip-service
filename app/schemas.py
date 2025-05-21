from pydantic import BaseModel, Field
from typing import List


class CoordPrediction(BaseModel):
    lat: float = Field(..., example=48.8584)
    lon: float = Field(..., example=2.2945)
    prob: float = Field(..., example=0.85)


class PredictResponse(BaseModel):
    predictions: List[CoordPrediction] = Field(
        ...,
        example={
            "predictions": [
                {"lat": 48.8584, "lon": 2.2945, "prob": 0.85},
                {"lat": 40.6892, "lon": -74.0445, "prob": 0.05}
            ]
        }
    )


class Match(BaseModel):
    id: str = Field(..., example="abc123")  # у тебя id — строка (Column(String))
    name: str = Field(..., example="Eiffel Tower")
    lat: float = Field(..., example=48.8584)
    lon: float = Field(..., example=2.2945)
    url: str = Field(..., example="https://example.com/images/eiffel.jpg")
    distance_km: float = Field(..., example=0.123)


class Сenter(BaseModel):
    lat: float = Field(..., example=48.8584)
    lon: float = Field(..., example=2.2945)


class NearbyResponse(BaseModel):
    center: Сenter = Field(
        ..., example={"lat": 48.8584, "lon": 2.2945}
    )
    matches: List[Match] = Field(
        ...,
        example=[
            {
                "id": "abc123",
                "name": "Eiffel Tower",
                "lat": 48.8584,
                "lon": 2.2945,
                "url": "https://example.com/images/eiffel.jpg",
                "distance_km": 0.123
            },
            {
                "id": "def456",
                "name": "Louvre Museum",
                "lat": 48.8606,
                "lon": 2.3376,
                "url": "https://example.com/images/louvre.jpg",
                "distance_km": 2.145
            }
        ]
    )
