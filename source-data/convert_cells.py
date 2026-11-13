import json
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "public" / "data"

def load(name):
    text = (HERE / "data" / name).read_text()
    # (Claude was used) keep only the JSON after "window.NAME =" and drop the final ";"
    return json.loads(text[text.index("=") + 1:].strip().rstrip(";"))


def square(lon, lat):
    # lon/lat is the south-west corner of a 1° cell
    ring = [[lon, lat], [lon + 1, lat], [lon + 1, lat + 1], [lon, lat + 1], [lon, lat]]
    return {"type": "Polygon", "coordinates": [ring]}


def save(name, features):
    OUT.mkdir(parents=True, exist_ok=True)
    geojson = {"type": "FeatureCollection", "features": features}
    (OUT / name).write_text(json.dumps(geojson, separators=(",", ":")))
    print(f"{name}: {len(features)} cells")


hyacinth = [
    {"type": "Feature", "geometry": square(lon, lat),
     "properties": {"records": n, "first": first, "last": last, "country": country}}
    for lon, lat, n, first, last, _inat, _spec, country in load("globe_cells.js")["cells"]
    if first is not None  # undated cells are hidden
]

save("hyacinth_cells.geojson", hyacinth)
