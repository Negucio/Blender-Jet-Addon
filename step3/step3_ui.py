import bpy
from .. common_utils import ApplyToSelected
from . step3_classes import Decimate

class VIEW3D_OT_jet_add_sufix(bpy.types.Operator):
    bl_idname = "add_sufix.btn"
    bl_label = "Add sufix"
    bl_description = "Add sufix to the selected objects"

    sufix = bpy.props.StringProperty(name="sufix",default="_Low")

    def execute(self, context):
        for obj in context.selected_objects:
            if self.sufix in obj.name: continue
            obj.name = obj.name + self.sufix
        return {'FINISHED'}

class VIEW3D_OT_jet_assign_decimate(bpy.types.Operator):
    bl_idname = "assign_decimate.btn"
    bl_label = "Assign Decimate"
    bl_description = "Assign Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        ApplyToSelected(context, self.decimate.AssignDecimate)
        return {'FINISHED'}

class VIEW3D_OT_jet_apply_decimate(bpy.types.Operator):
    bl_idname = "apply_decimate.btn"
    bl_label = "Apply Decimate"
    bl_description = "Apply Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        ApplyToSelected(context, self.decimate.ApplyDecimate)
        return {'FINISHED'}

class VIEW3D_PT_jet_step3(bpy.types.Panel):
    bl_label = "Step 3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Hi-res Model Prep")
        layout.operator("assign_decimate.btn", text="Assign Decimate")
        layout.operator("apply_decimate.btn", text="Apply Decimate")
        layout.operator("add_sufix.btn", text="Add Sufix '_Low'").sufix = "_Low"
        layout.operator("add_sufix.btn", text="Add Sufix '_High'").sufix = "_High"
