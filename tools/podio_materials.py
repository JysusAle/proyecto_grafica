"""Asigna materiales al podio (el .blend no tenia ninguno -> salia negro).

Uso:
    blender -b podio-y-trofeo.blend --python tools/podio_materials.py

Se ejecuta antes de export_obj.py, que toma el color base de cada material
para generar la textura que usa OpenGL.
"""

import bpy

PALETA = {
    "Gold":   (0.85, 0.68, 0.22, 1.0),  # trofeo
    "Red":    (0.72, 0.06, 0.06, 1.0),  # franja del podio
    "White":  (0.92, 0.92, 0.90, 1.0),  # gradas del podio
}

# objeto -> material (Cilindro = trofeo, Cubo = base, Cubo.001 = escalon)
ASIGNACION = {
    "Cilindro": "Gold",
    "Cubo": "Red",
    "Cubo.001": "White",
}


def get_material(name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is not None:
        bsdf.inputs["Base Color"].default_value = PALETA[name]
    mat.diffuse_color = PALETA[name]
    return mat


for obj_name, mat_name in ASIGNACION.items():
    ob = bpy.data.objects.get(obj_name)
    if ob is None or ob.type != "MESH":
        print("NO ENCONTRADO:", obj_name)
        continue
    ob.data.materials.clear()
    ob.data.materials.append(get_material(mat_name))
    print("MATERIAL", obj_name, "->", mat_name)

print("MATERIALES ASIGNADOS")
