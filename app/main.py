from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from db import init_db, SessionLocal
from database import search_nearby
from model import load_model, predict_topk
import uvicorn
import tempfile
from schemas import PredictResponse, NearbyResponse

app = FastAPI(
    title="GeoCLIP API",
    description="""
GeoCLIP — API-сервис для геолокации по изображениям на основе модели CLIP.

## Возможности:

- 📍 Предсказание координат по изображению
- 📷 Поиск похожих изображений в радиусе
- 🧪 Примеры запросов
    """,
    openapi_tags=[
        {"name": "Prediction", "description": "Эндпоинты для предсказания координат"},
        {"name": "Search", "description": "Поиск изображений поблизости"},
        {"name": "Examples", "description": "Примеры запросов"},
    ]
)


@app.on_event("startup")
def on_startup():
    # Создаём таблицы в БД при старте приложения
    init_db()


# Загружаем модель один раз при старте
model = load_model()


@app.post(
    "/predict/coords",
    response_model=PredictResponse,
    tags=["Prediction"],
    summary="Предсказание координат",
    description="""
Принимает изображение и возвращает топ-K наиболее вероятных координат с вероятностями.

- **top_k**: количество координат в ответе (от 1 до 10)
- **file**: изображение (jpg/png)
"""
)
async def coords_endpoint(file: UploadFile = File(...), description="Файл изображения (.jpg/.png)",
                          top_k: int = Query(1, ge=1, le=10,
                                             description="Количество координат (top-K)")):
    contents = await file.read()
    try:
        # Создаём временный файл, чтобы передать путь в predict_topk
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
            tmp.write(contents)
            tmp.flush()

            coords, probs = predict_topk(model, tmp.name, top_k=top_k)

        # Гарантируем, что всё — Python float
        response = [
            {"lat": float(lat), "lon": float(lon), "prob": float(p)}
            for (lat, lon), p in zip(coords, probs)
        ]
        return {"predictions": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/health",
    tags=["Examples"],
    summary="Проверка работоспособности",
    description="Простой health-check для проверки, что сервис живой."
)
def health():
    return {"status": "ok"}


@app.post(
    "/search/nearby",
    response_model=NearbyResponse,
    tags=["Search"],
    summary="Поиск изображений поблизости от предсказанной точки",
    description="""
Принимает изображение и возвращает изображения из базы, находящиеся в радиусе от предсказанной координаты.

- **radius_km**: радиус поиска в километрах
"""
)
async def nearby_endpoint(
        file: UploadFile = File(...),
        radius_km: float = Query(10.0, ge=0, le=10000, description="Радиус поиска в километрах")
):
    contents = await file.read()
    try:
        # Временный файл для инференса
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
            tmp.write(contents)
            tmp.flush()

            # Получаем центр (lat, lon)
            coords, _ = predict_topk(model, tmp.name, top_k=1)
            center = coords[0]

        # Открываем сессию к БД
        db: Session = SessionLocal()
        matches = search_nearby(center, radius_km, db)
        db.close()

        return {
            "center": {"lat": float(center[0]), "lon": float(center[1])},
            "matches": matches
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/examples/nearby",
    response_model=NearbyResponse,
    tags=["Examples"],
    summary="Пример: Поиск из базы по координатам",
    description="""
Принимает координаты (lat, lon) и возвращает изображения поблизости из базы.

- **lat**: широта [-90, 90]
- **lon**: долгота [-180, 180]
- **radius_km**: радиус поиска
"""
)
async def examples_nearby(
        lat: float = Query(..., ge=-90.0, le=90.0, description="Широта [-90, 90]"),
        lon: float = Query(..., ge=-180.0, le=180.0, description="Долгота [-180, 180]"),
        radius_km: float = Query(10.0, ge=0, le=10000, description="Радиус поиска (0–10000 км)")
):
    try:
        center = (lat, lon)
        db: Session = SessionLocal()
        matches = search_nearby(center, radius_km, db)
        db.close()
        return {
            "center": {"lat": lat, "lon": lon},
            "matches": matches
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
