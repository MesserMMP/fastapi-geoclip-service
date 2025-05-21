from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from db import SessionLocal, Image
import math


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Возвращает расстояние между двумя точками на Земле по формуле Haversine (в км).
    """
    R = 6371.0  # радиус Земли в км
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def search_nearby(center: Tuple[float, float],
                  radius_km: float,
                  db: Session) -> List[Dict]:
    """
    Ищет в DB все записи внутри radius_km от center (lat, lon).
    Возвращает список словарей с полями id, lat, lon, url и distance_km.
    """
    lat0, lon0 = center
    results: List[Dict] = []
    for img in db.query(Image).all():
        dist = haversine(lat0, lon0, img.lat, img.lon)
        if dist <= radius_km:
            results.append({
                "id": img.id,
                "name": img.name,
                "lat": img.lat,
                "lon": img.lon,
                "url": img.url,
                "distance_km": round(dist, 3)
            })
    results.sort(key=lambda x: x["distance_km"])
    return results
