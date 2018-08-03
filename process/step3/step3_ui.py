import bpy
from ... common_utils import apply_to_selected
from . step3_utils import EnableAndConfigAutosmooth, ManageSharp

#Panel
class VIEW3D_PT_jet_step3(bpy.types.Panel):
    bl_label = "Step 3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Smoothing and Sharpening")

        col = layout.column(align=True)
        col.operator("object.shade_smooth", text="Smooth")
        col.operator("jet_autosmooth.btn", text="Enable Autosmooth")
        col.label("-Slider for AutoSmooth")
        col.label("-Tag Sharp Enable (Ctrl+RMB to Tag)")
        row = col.row(align=True)
        row.operator("jet_sharp.btn", text="Mark Sharp").mark = True
        row.operator("jet_sharp.btn", text="Clear Sharp").mark = False


#Operators
class VIEW3D_OT_jet_autosmooth(bpy.types.Operator):
    bl_idname = "jet_autosmooth.btn"
    bl_label = "Autosmooth"
    bl_description = "Enable Autosmooth and set the smooth angle to 180"

    def execute(self, context):
        apply_to_selected(context, EnableAndConfigAutosmooth)
        return {'FINISHED'}

class VIEW3D_OT_jet_sharp(bpy.types.Operator):
    bl_idname = "jet_sharp.btn"
    bl_label = "Sharp"
    bl_description = "Manage Sharp"

    mark = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        ManageSharp(context, self.mark)
        return {'FINISHED'}