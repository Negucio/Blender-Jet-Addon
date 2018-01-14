import bpy
from . step2_ui import \
    VIEW3D_PT_jet_step2, \
    VIEW3D_OT_jet_triangulate

def register():
    bpy.utils.register_class(VIEW3D_OT_jet_triangulate)
    bpy.utils.register_class(VIEW3D_PT_jet_step2)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_jet_step2)
    bpy.utils.unregister_class(VIEW3D_OT_jet_triangulate)

