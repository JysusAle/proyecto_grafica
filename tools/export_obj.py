"""Exporta un .blend del proyecto a .obj + .mtl + texturas para OpenGL.

Uso:
    blender -b archivo.blend --python tools/export_obj.py -- /ruta/salida/archivo.obj

Pasos:
  1. Crea una textura PNG por material (color base de Blender + ruido) y la
     conecta al BSDF, para que Assimp encuentre un map_Kd en el .mtl.
  2. Genera coordenadas UV (smart project) en cada malla que no tenga.
  3. Exporta el .obj con ejes de OpenGL: Y arriba, -Z al frente.
"""

import math
import os
import random
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not argv:
    print("FALTA la ruta de salida: -- /ruta/salida/archivo.obj")
    sys.exit(1)

out_abs = os.path.abspath(os.path.expanduser(argv[0]))
tex_dir = os.path.dirname(out_abs)
os.makedirs(tex_dir, exist_ok=True)


def make_texture(mat, size=256, noise=0.08):
    """Imagen con el color del material + ruido, guardada junto al .obj."""
    safe = "".join(c if c.isalnum() else "_" for c in mat.name)
    name = "tex_" + safe
    path = os.path.join(tex_dir, name + ".png")

    img = bpy.data.images.get(name)
    if img is None:
        img = bpy.data.images.new(name, size, size, alpha=False, float_buffer=False)
        r, g, b = mat.diffuse_color[:3]
        rnd = random.Random(sum(ord(c) for c in name))
        px = []
        for _ in range(size * size):
            n = (rnd.random() - 0.5) * 2.0 * noise
            px.extend([
                min(1.0, max(0.0, r + n)),
                min(1.0, max(0.0, g + n)),
                min(1.0, max(0.0, b + n)),
                1.0,
            ])
        img.pixels = px

    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    img.filepath = path
    return img


def texture_materials():
    total = 0
    for mat in bpy.data.materials:
        if mat.node_tree is None:
            continue
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
        if bsdf is None:
            continue

        tex = next((n for n in nodes if n.type == "TEX_IMAGE"), None)
        if tex is None or tex.image is None:
            tex = nodes.new("ShaderNodeTexImage")
            tex.image = make_texture(mat)
            tex.location = (-420, 200)
        base = bsdf.inputs.get("Base Color")
        if base is not None and not base.is_linked:
            links.new(tex.outputs["Color"], base)
        total += 1
    return total


def ensure_uvs():
    done = 0
    for ob in bpy.data.objects:
        if ob.type != "MESH" or len(ob.data.uv_layers) > 0:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=math.radians(66.0),
                                  island_margin=0.02,
                                  correct_aspect=True,
                                  scale_to_bounds=False)
        bpy.ops.object.mode_set(mode="OBJECT")
        apply_uv_scale(ob)
        done += 1
    bpy.ops.object.select_all(action="DESELECT")
    return done


# Escala de UV por material: hace que la textura se repita a una escala
# fisica razonable (sin esto una textura cubre la isla completa y se ve borrosa).
UV_SCALE = {
    "Grass": 6.0,
    "Pavement": 5.0,
    "Concrete": 1.5,
    "Roof": 4.0,
    "Metal": 3.0,
}


def apply_uv_scale(ob):
    mesh = ob.data
    uv = mesh.uv_layers.active
    if uv is None:
        return
    # Los loops no traen polygon directo: se recorre por cara.
    for poly in mesh.polygons:
        s = UV_SCALE.get(mesh.materials[poly.material_index].name, 1.0) if poly.material_index < len(mesh.materials) else 1.0
        if s == 1.0:
            continue
        for li in poly.loop_indices:
            u, v = uv.data[li].uv
            uv.data[li].uv = (u * s, v * s)


n_mat = texture_materials()
n_uv = ensure_uvs()

bpy.ops.wm.obj_export(
    filepath=out_abs,
    forward_axis="NEGATIVE_Z",
    up_axis="Y",
    global_scale=1.0,
    apply_modifiers=True,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=False,
    export_object_groups=False,
    export_material_groups=False,
    path_mode="COPY",
)

print("EXPORTADO:", out_abs)
print("MATERIALES TEXTURIZADOS:", n_mat, "| MALLAS CON UV NUEVAS:", n_uv)
print("OBJETOS:", len([o for o in bpy.data.objects if o.type == "MESH"]))
