import bpy, bmesh
from .. common_utils import SelectObjectExclusive


def triangulate(obj):
    if obj == None or obj.type != "MESH": return None
    SelectObjectExclusive(obj, edit_mode=True)

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bmesh.ops.triangulate(bm, faces=bm.faces)

    bpy.ops.object.mode_set(mode="OBJECT")
