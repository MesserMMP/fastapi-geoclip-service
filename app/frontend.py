import os
import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(layout="wide")
st.title("GeoCLIP Viewer")

st.sidebar.header("Options")
mode = st.sidebar.selectbox("Select operation", ["Predict Coords", "Search Nearby", "Examples Nearby"])


def file_to_base64(file):
    file.seek(0)
    data = file.read()
    encoded = base64.b64encode(data).decode()
    return f"data:image/png;base64,{encoded}"


def create_map(center, points, center_label="Center", center_img_data=None):
    center_loc = [center["lat"], center["lon"]]

    m = folium.Map(location=center_loc, zoom_start=5, tiles="CartoDB positron")

    if center_img_data:
        # Увеличенный tooltip с картинкой для центра
        tooltip_html = f"""
        <div style="width: 350px;">
            <b>{center_label}</b><br>
            <img src="{center_img_data}" width="300" />
        </div>
        """
        folium.Marker(
            location=center_loc,
            icon=folium.Icon(color="red", icon="star"),
            tooltip=folium.Tooltip(tooltip_html, sticky=True, direction='right'),
        ).add_to(m)
    else:
        folium.Marker(
            location=center_loc,
            popup=folium.Popup(f"<b>{center_label}</b>", max_width=350),
            icon=folium.Icon(color="red", icon="star"),
            tooltip=center_label,
        ).add_to(m)

    for p in points:
        tooltip_html = f"""
        <div style="width: 350px;">
            <b>{p['name']}</b><br>
            Distance: {p['distance_km']:.2f} km<br>
            <img src="{p['url']}" width="300" />
        </div>
        """
        folium.Marker(
            location=[p["lat"], p["lon"]],
            icon=folium.Icon(color="blue", icon="info-sign"),
            tooltip=folium.Tooltip(tooltip_html, sticky=True, direction='right'),
        ).add_to(m)

    return m


def create_map_preds(center, points, center_label="Center"):
    center_loc = [center["lat"], center["lon"]]

    m = folium.Map(location=center_loc, zoom_start=5, tiles="CartoDB positron")

    folium.Marker(
        location=center_loc,
        popup=folium.Popup(f"<b>{center_label}</b>", max_width=250),
        icon=folium.Icon(color="red", icon="star"),
        tooltip=center_label,
    ).add_to(m)

    for idx, p in enumerate(points):
        popup_html = f"""
        <b>Prediction #{idx + 1}</b><br>
        Probability: {p.get('prob', 0):.3f}<br>
        Lat: {p['lat']:.6f}<br>
        Lon: {p['lon']:.6f}
        """
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign"),
            tooltip=f"Prediction #{idx + 1}",
        ).add_to(m)

    return m


if mode == "Predict Coords":
    st.header("Predict Coordinates from Image")
    uploaded_file = st.file_uploader("Upload image", type=["jpg", "png"])
    top_k = st.slider("Top K", 1, 10, 1)

    if "preds" not in st.session_state:
        st.session_state.preds = None
        st.session_state.img = None

    if uploaded_file and st.button("Predict"):
        response = requests.post(
            f"{API_URL}/predict/coords",
            params={"top_k": top_k},
            files={"file": uploaded_file},
        )
        if response.ok:
            data = response.json()
            st.session_state.preds = data["predictions"]
            st.session_state.img = uploaded_file  # сохраним файл в состоянии
        else:
            st.error(response.text)
            st.session_state.preds = None
            st.session_state.img = None

    if st.session_state.preds:
        preds = st.session_state.preds
        center = preds[0]

        # Отобразить карту с предсказаниями
        m = create_map_preds(center, preds, center_label="Predicted Points")
        st_folium(m, width=1000, height=500)

        # Отобразить загруженное изображение
        if st.session_state.img:
            st.image(st.session_state.img, caption="Uploaded Image", width=500)

        # Отобразить таблицу с предсказанными координатами
        st.write("Predicted Coordinates:")
        st.dataframe(pd.DataFrame(preds))


elif mode == "Search Nearby":
    st.header("Search Images Nearby Predicted Point")
    uploaded_file = st.file_uploader("Upload image", type=["jpg", "png"])
    radius_km = st.number_input("Radius (km)", min_value=0.1, max_value=10000.0, value=10.0)

    if uploaded_file:
        if "search_result" not in st.session_state:
            st.session_state.search_result = None

        if st.button("Search"):
            response = requests.post(f"{API_URL}/search/nearby", params={"radius_km": radius_km},
                                     files={"file": uploaded_file})
            if response.ok:
                st.session_state.search_result = response.json()
            else:
                st.error(response.text)

        if st.session_state.search_result:
            data = st.session_state.search_result
            center = data["center"]
            matches = data["matches"]

            # Подготовить base64 для картинки центра (для tooltip)
            center_img_data = file_to_base64(uploaded_file) if uploaded_file else None

            df_center = pd.DataFrame([center])
            df_center["distance_km"] = 0.0
            df_center["name"] = "Predicted Point"
            df_center_display = df_center[["name", "lat", "lon", "distance_km"]]

            df_matches = pd.DataFrame(matches)
            df_matches_display = df_matches.drop(columns=["id", "url"], errors="ignore")

            st.write("Center and Matches:")
            st.dataframe(pd.concat([df_center_display, df_matches_display], ignore_index=True))

            # Карта с изображением при наведении на центр
            m = create_map(center, matches, center_label="Predicted Point", center_img_data=center_img_data)
            st_folium(m, width=1000, height=500)

            # Сначала выводим загруженное изображение
            st.write("Uploaded Image:")
            st.image(uploaded_file, width=500)

            # Затем найденные изображения
            st.write("Nearby Images:")
            for match in matches:
                st.write(f"**{match['name']}** ({match['distance_km']:.2f} km)")
                st.image(match["url"], width=500)


else:  # Examples Nearby
    st.header("Examples Nearby by Coordinates")
    lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=52.51653)
    lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=13.3775)
    radius_km = st.number_input("Radius (km)", min_value=0.1, max_value=10000.0, value=10.0)

    if "examples_result" not in st.session_state:
        st.session_state.examples_result = None

    if st.button("Get Examples"):
        params = {"lat": lat, "lon": lon, "radius_km": radius_km}
        response = requests.get(f"{API_URL}/examples/nearby", params=params)
        if response.ok:
            st.session_state.examples_result = response.json()
        else:
            st.error(response.text)

    if st.session_state.examples_result:
        data = st.session_state.examples_result
        center = data["center"]
        matches = data["matches"]

        df_center = pd.DataFrame([center])
        df_center["distance_km"] = 0.0
        df_center["name"] = "Predicted Point"
        df_center_display = df_center[["name", "lat", "lon", "distance_km"]]

        df_matches = pd.DataFrame(matches)
        df_matches_display = df_matches.drop(columns=["id", "url"], errors="ignore")

        st.write("Center and Matches:")
        st.dataframe(pd.concat([df_center_display, df_matches_display], ignore_index=True))

        m = create_map(center, matches, center_label="Selected Point")
        st_folium(m, width=1000, height=500)

        st.write("Nearby Images:")
        for match in matches:
            st.write(f"**{match['name']}** ({match['distance_km']:.2f} km)")
            st.image(match["url"], width=500)
