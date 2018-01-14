import bpy
from .. common_utils import ApplyToSelected
from . step2_utils import triangulate

class VIEW3D_OT_jet_triangulate(bpy.types.Operator):
    bl_idname = "jet_triangulate.btn"
    bl_label = "Triangulate"
    bl_description = "Triangulate"

    def execute(self, context):
        ApplyToSelected(context, triangulate)
        return {'FINISHED'}

class VIEW3D_PT_jet_step2(bpy.types.Panel):
    bl_label = "Step 2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("UVs completas")
        layout.label("TODO: Texture Atlas")
        layout.operator("jet_triangulate.btn", text="Triangulate")
