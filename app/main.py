from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from database import search_nearby
from model import load_model, predict_topk
import uvicorn
import tempfile

app = FastAPI(title="GeoCLIP API")

# Загружаем модель один раз при старте
model = load_model()


@app.post("/predict/coords")
async def coords_endpoint(file: UploadFile = File(...), top_k: int = 1):
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
        response = []
        for (lat, lon), p in zip(coords, probs):
            response.append({
                "lat": float(lat),
                "lon": float(lon),
                "prob": float(p)
            })

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

        # Ищем по in-memory БД
        matches = search_nearby(center, radius_km)
        return {
            "center": {"lat": float(center[0]), "lon": float(center[1])},
            "matches": matches
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
