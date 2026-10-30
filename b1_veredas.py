import geopandas as gpd
import requests


# ============================================================
# B1 — VEREDAS DE BOYACÁ
# ============================================================

# ------------------------------------------------------------
# PARTE 1 — Descargar veredas de Tunja mediante requests
# ------------------------------------------------------------

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson",
}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()

gdf_tunja = gpd.GeoDataFrame.from_features(
    r.json()["features"],
    crs=4326
)

print("PARTE 1 — Veredas de Tunja")
print("---------------------------")
print("Número de veredas:", len(gdf_tunja))


# ------------------------------------------------------------
# PARTE 2 — Veredas por municipio
# ------------------------------------------------------------

gdf = gpd.read_file("datos/veredas_boyaca.geojson")

por_municipio = (
    gdf.groupby("NOMB_MPIO")
    .size()
    .sort_values(ascending=False)
)

print()
print("PARTE 2 — Top 10 municipios por número de veredas")
print("---------------------------------------------------")

print(por_municipio.head(10))


# ------------------------------------------------------------
# PARTE 3 — Área de las veredas
# ------------------------------------------------------------

gdf_m = gdf.to_crs(9377)

gdf_m["area_ha"] = gdf_m.geometry.area / 10000

mayores_veredas = (
    gdf_m[["NOMB_MPIO", "NOMBRE_VER", "area_ha"]]
    .sort_values("area_ha", ascending=False)
    .head(5)
)

print()
print("PARTE 3 — Las 5 veredas más grandes")
print("------------------------------------")

print(mayores_veredas.to_string(index=False))