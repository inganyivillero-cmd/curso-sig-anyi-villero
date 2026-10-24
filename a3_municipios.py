import json
from collections import Counter

# Leer el GeoJSON
with open("datos/provincias_boyaca.geojson", encoding="utf-8") as f:
    datos = json.load(f)

# -----------------------------
# PARTE 1 — SIN PANDAS
# -----------------------------

conteo = Counter(
    feat["properties"]["provincia"]
    for feat in datos["features"]
)

print("PARTE 1 — Municipios por provincia")
print("-----------------------------------")

for provincia, n in conteo.most_common():
    print(f"{provincia:20} {n}")


# -----------------------------
# PARTE 2 — CON PANDAS
# -----------------------------

import pandas as pd

props = [f["properties"] for f in datos["features"]]

df = pd.DataFrame(props)

print()
print("PARTE 2 — Municipios por provincia con pandas")
print("----------------------------------------------")

print(
    df.groupby("provincia")
    .size()
    .sort_values(ascending=False)
)


# -----------------------------
# PREGUNTA DE CIERRE
# -----------------------------

print()
print("Número de provincias distintas:", df["provincia"].nunique())