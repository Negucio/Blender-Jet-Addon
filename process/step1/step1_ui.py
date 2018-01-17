import bpy
from ... common_utils import apply_to_selected
from . step1_utils import EnableAndConfigAutosmooth, SharpToSeam, Unwrap, ManageSharp, ManageSeam

#Panel
class VIEW3D_PT_jet_step1(bpy.types.Panel):
    bl_label = "Step 1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Preparación Modelo")
        layout.operator("jet_autosmooth.btn", text="Enable Autosmooth")
        row = layout.row(align=True)
        row.operator("jet_sharp.btn", text="Mark Sharp").mark = True
        row.operator("jet_sharp.btn", text="Clear Sharp").mark = False
        row = layout.row(align=True)
        row.operator("jet_seam.btn", text="Mark Seam").mark = True
        row.operator("jet_seam.btn", text="Clear Seam").mark = False
        layout.operator("jet_sharp_to_seam.btn", text="Mark Sharp as Seam")
        layout.label("UVs individuales")
        layout.operator("jet_unwrap.btn", text="Unwrap")


#Operators
class VIEW3D_OT_jet_autosmooth(bpy.types.Operator):
    bl_idname = "jet_autosmooth.btn"
    bl_label = "Autosmooth"
    bl_description = "Enable Autosmooth and set the smooth angle to 180"

    def execute(self, context):
        apply_to_selected(context, EnableAndConfigAutosmooth)
        return {'FINISHED'}

class VIEW3D_OT_jet_sharp_to_seam(bpy.types.Operator):
    bl_idname = "jet_sharp_to_seam.btn"
    bl_label = "Sharp to Seam"
    bl_description = "Mark Sharp edges as Seam"

    def execute(self, context):
        apply_to_selected(context, SharpToSeam)
        return {'FINISHED'}

class VIEW3D_OT_jet_unwrap(bpy.types.Operator):
    bl_idname = "jet_unwrap.btn"
    bl_label = "Unwrap"
    bl_description = "Unwrap"

    def execute(self, context):
        apply_to_selected(context, Unwrap)
        return {'FINISHED'}


class VIEW3D_OT_jet_sharp(bpy.types.Operator):
    bl_idname = "jet_sharp.btn"
    bl_label = "Sharp"
    bl_description = "Manage Sharp"

    mark = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        ManageSharp(context, self.mark)
        return {'FINISHED'}

class VIEW3D_OT_jet_seam(bpy.types.Operator):
    bl_idname = "jet_seam.btn"
    bl_label = "Seam"
    bl_description = "Manage Seam"

    mark = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        ManageSeam(context, self.mark)
        return {'FINISHED'}








