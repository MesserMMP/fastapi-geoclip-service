import math
from typing import List, Tuple, Dict

# Пример: три изображения с координатами и ссылками
METADATA: List[Tuple[str, str, float, float, str]] = [
    # (id, name,   lat,     lon,     url)
    ("img001", "Eiffel Tower", 48.8584, 2.2945, "https://example.com/eiffel.jpg"),
    ("img002", "Statue of Liberty", 40.6892, -74.0445, "https://example.com/liberty.jpg"),
    ("img003", "Big Ben", 51.5007, -0.1246, "https://example.com/bigben.jpg"),
]


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


def search_nearby(center: Tuple[float, float], radius_km: float) -> List[Dict]:
    """
    Ищет в METADATA все записи внутри radius_km от center (lat, lon).
    Возвращает список словарей с полями id, lat, lon, url и distance_km.
    """
    lat0, lon0 = center
    results: List[Dict] = []
    for img_id, name, lat, lon, url in METADATA:
        dist = haversine(lat0, lon0, lat, lon)
        if dist <= radius_km:
            results.append({
                "id": img_id,
                "name": name,
                "lat": lat,
                "lon": lon,
                "url": url,
                "distance_km": round(dist, 3)
            })
    results.sort(key=lambda x: x["distance_km"])
    return results
