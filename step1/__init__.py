import bpy
from . step1_ui import  \
    VIEW3D_PT_jet_step1, \
    VIEW3D_OT_jet_autosmooth, \
    VIEW3D_OT_jet_sharp_to_seam, \
    VIEW3D_OT_jet_unwrap, \
    VIEW3D_OT_jet_sharp, \
    VIEW3D_OT_jet_seam

def register():
    bpy.utils.register_class(VIEW3D_OT_jet_autosmooth)
    bpy.utils.register_class(VIEW3D_OT_jet_sharp_to_seam)
    bpy.utils.register_class(VIEW3D_OT_jet_unwrap)
    bpy.utils.register_class(VIEW3D_OT_jet_sharp)
    bpy.utils.register_class(VIEW3D_OT_jet_seam)
    bpy.utils.register_class(VIEW3D_PT_jet_step1)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_jet_step1)
    bpy.utils.unregister_class(VIEW3D_OT_jet_autosmooth)
    bpy.utils.unregister_class(VIEW3D_OT_jet_sharp_to_seam)
    bpy.utils.unregister_class(VIEW3D_OT_jet_unwrap)
    bpy.utils.unregister_class(VIEW3D_OT_jet_sharp)
    bpy.utils.unregister_class(VIEW3D_OT_jet_seam)
