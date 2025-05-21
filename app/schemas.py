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
    id: int = Field(..., example=123)
    lat: float = Field(..., example=48.8584)
    lon: float = Field(..., example=2.2945)
    path: str = Field(..., example="/images/eiffel.jpg")


class NearbyResponse(BaseModel):
    center: CoordPrediction = Field(
        ..., example={"lat": 48.8584, "lon": 2.2945, "prob": 0.85}
    )
    matches: List[Match] = Field(
        ...,
        example=[
            {
                "id": 123,
                "lat": 48.8584,
                "lon": 2.2945,
                "path": "/images/eiffel.jpg"
            },
            {
                "id": 124,
                "lat": 48.8575,
                "lon": 2.2950,
                "path": "/images/eiffel2.jpg"
            }
        ]
    )
