
import requests

# Endpoint del servicio REST de veredas de Boyacá
url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"

# Parámetros generales de la consulta
base = {
    "where": "1=1",
    "outFields": "NOMB_MPIO,NOMBRE_VER",
    "outSR": "4326",
    "f": "geojson"
}

# Tamaño del bloque: primero 1000 y luego 500
bloque = 500

features = []
offset = 0

print("B2 — PAGINACIÓN DE VEREDAS DE BOYACÁ")
print("--------------------------------------")

while True:
    parametros = {
        **base,
        "resultOffset": offset,
        "resultRecordCount": bloque
    }

    respuesta = requests.get(url, params=parametros, timeout=30)
    respuesta.raise_for_status()
    datos = respuesta.json()

    if "error" in datos:
        raise Exception(datos["error"])

    nuevos = datos.get("features", [])
    features.extend(nuevos)

    print(f"Offset {offset}: +{len(nuevos)} registros (total: {len(features)})")

    if len(nuevos) < bloque:
        break

    offset += bloque

# Total de veredas recuperadas
print("\nTOTAL DE VEREDAS:", len(features))

# Cantidad de municipios distintos
municipios = {
    f["properties"].get("NOMB_MPIO")
    for f in features
    if f["properties"].get("NOMB_MPIO")
}

print("MUNICIPIOS DISTINTOS:", len(municipios))
