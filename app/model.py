import torch
from geoclip import GeoCLIP
from typing import List, Tuple


def load_model(device: str = None) -> GeoCLIP:
    """
    Загружает модель GeoCLIP на указанный девайс (CPU/GPU).
    """
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    model = GeoCLIP().to(device)
    model.eval()
    return model


def predict_topk(model: GeoCLIP, image_path: str, top_k: int = 3) -> Tuple[List[Tuple[float, float]], List[float]]:
    """
    Выполняет инференс на заданном изображении и возвращает:
    - список топ-K GPS координат [(lat, lon), ...]
    - соответствующие вероятности [p1, p2, ...]
    """
    top_pred_gps, top_pred_prob = model.predict(image_path, top_k=top_k)
    return top_pred_gps, top_pred_prob
