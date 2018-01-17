import bpy
from . step3_ui import \
    VIEW3D_PT_jet_step3, \
    VIEW3D_OT_jet_add_sufix, \
    VIEW3D_OT_jet_assign_decimate, \
    VIEW3D_OT_jet_apply_decimate, \
    VIEW3D_OT_jet_apply_modifiers, \
    VIEW3D_OT_jet_remove_parent


def register():
    bpy.utils.register_class(VIEW3D_OT_jet_add_sufix)
    bpy.utils.register_class(VIEW3D_OT_jet_assign_decimate)
    bpy.utils.register_class(VIEW3D_OT_jet_apply_decimate)
    bpy.utils.register_class(VIEW3D_OT_jet_apply_modifiers)
    bpy.utils.register_class(VIEW3D_OT_jet_remove_parent)
    bpy.utils.register_class(VIEW3D_PT_jet_step3)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_jet_step3)
    bpy.utils.unregister_class(VIEW3D_OT_jet_add_sufix)
    bpy.utils.unregister_class(VIEW3D_OT_jet_assign_decimate)
    bpy.utils.unregister_class(VIEW3D_OT_jet_apply_decimate)
    bpy.utils.unregister_class(VIEW3D_OT_jet_apply_modifiers)
    bpy.utils.unregister_class(VIEW3D_OT_jet_remove_parent)
