import bpy, bmesh
from ... common_utils import select_obj_exclusive
from addon_utils import check, enable, modules_refresh

def is_texture_atlas_enabled():
    is_enabled, is_loaded = check("uv_texture_atlas")
    return is_enabled

def handle_error(ex):
    print("Error loading Texture Atlas Addon: " + ex)

def enable_texture_atlas():
    enable("uv_texture_atlas", default_set=True, persistent=True, handle_error=handle_error)

def triangulate(obj):
    if obj == None or obj.type != "MESH": return None
    select_obj_exclusive(obj, edit_mode=True)

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bmesh.ops.triangulate(bm, faces=bm.faces)

    bpy.ops.object.mode_set(mode="OBJECT")
