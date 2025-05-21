from fastapi import FastAPI, File, UploadFile, HTTPException
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
