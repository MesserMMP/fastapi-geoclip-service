from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from db import init_db, SessionLocal
from database import search_nearby
from model import load_model, predict_topk
import uvicorn
import tempfile

app = FastAPI(title="GeoCLIP API")


@app.on_event("startup")
def on_startup():
    # Создаём таблицы в БД при старте приложения
    init_db()


# Загружаем модель один раз при старте
model = load_model()


@app.post("/predict/coords")
async def coords_endpoint(file: UploadFile = File(...),
                          top_k: int = Query(1, ge=1, le=10,
                                             description="Количество координат (top-K)")):
    """
    Принимает изображение, возвращает топ-K координат и вероятностей.
    """
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search/nearby")
async def nearby_endpoint(
        file: UploadFile = File(...),
        radius_km: float = Query(10.0, ge=0, le=10000, description="Радиус поиска в километрах")
):
    """
    Принимает изображение, возвращает ближайшие из предзагруженной БД
    изображения в радиусе radius_km км от предсказанной точки.
    """
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


from fastapi import Query


@app.get("/examples/nearby")
async def examples_nearby(
        lat: float = Query(..., ge=-90.0, le=90.0, description="Широта [-90, 90]"),
        lon: float = Query(..., ge=-180.0, le=180.0, description="Долгота [-180, 180]"),
        radius_km: float = Query(10.0, ge=0, le=10000, description="Радиус поиска (0–10000 км)")
):
    """
    Возвращает изображения из базы, находящиеся в радиусе radius_km от заданной точки (lat, lon).
    """
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
