"""Genera las texturas finales de Models/ a partir de las base de Poly Haven.

Uso (despues de exportar el .obj, porque export_obj.py sobrescribe los PNG):
    python3 tools/aplicar_texturas.py

Base (CC0, https://polyhaven.com) en tools/texturas_base/:
    leafy_grass              -> tex_Grass.png    (teñido a verde de cancha)
    asphalt_06               -> tex_Pavement.png (plaza)
    brushed_concrete_03      -> tex_Concrete.png (fachada, neutro y sin grano)
    box_profile_metal_sheet  -> tex_Roof.png      (cubierta plata)
"""

import os

import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "texturas_base")
MODELS = os.path.join(os.path.dirname(AQUI), "Models")
SIZE = 1024


def cargar(nombre):
    ruta = os.path.join(BASE, nombre)
    im = Image.open(ruta).convert("RGB")
    if im.size != (SIZE, SIZE):
        im = im.resize((SIZE, SIZE), Image.LANCZOS)
    return im


def luma(arr):
    return 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]


def normalizar(arr):
    lo, hi = arr.min(), arr.max()
    return (arr - lo) / max(1e-6, hi - lo)


def guardar(arr, nombre):
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype("uint8")).save(
        os.path.join(MODELS, nombre))
    px = list(Image.open(os.path.join(MODELS, nombre)).resize((32, 32)).getdata())
    prom = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    print("%-20s %s" % (nombre, prom))


def main():
    # Plaza: concreto claro de Poly Haven, tal cual
    guardar(np.asarray(cargar("asphalt_06.jpg"), dtype=np.float32) / 255.0,
            "tex_Pavement.png")

    # Fachada: mismo concreto pero neutro (sin tinte marron) y sin el grano
    # fino que a distancia se ve como "estatica".
    concreto = cargar("brushed_concrete_03.jpg").filter(ImageFilter.GaussianBlur(1.2))
    c = np.asarray(concreto, dtype=np.float32) / 255.0
    g = 0.45 + 0.55 * normalizar(luma(c))          # contraste suave
    guardar(g[..., None] * np.array([0.80, 0.81, 0.83]), "tex_Concrete.png")

    # Cesped: hojas de cesped reales teñidas al verde de cancha regada
    h = np.asarray(cargar("leafy_grass.jpg"), dtype=np.float32) / 255.0
    g = 0.62 + 0.38 * normalizar(luma(h))
    guardar(g[..., None] * np.array([0.30, 0.62, 0.20]) * 1.35, "tex_Grass.png")

    # Cubierta: perfil metalico teñido a gris plata claro
    m = np.asarray(cargar("box_profile_metal_sheet.jpg"), dtype=np.float32) / 255.0
    g = 0.75 + 0.25 * normalizar(luma(m))
    guardar(g[..., None] * np.array([0.88, 0.89, 0.90]), "tex_Roof.png")


if __name__ == "__main__":
    main()
