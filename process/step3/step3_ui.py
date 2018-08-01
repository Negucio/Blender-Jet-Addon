import bpy

from . step3_utils import apply_modifiers, remove_parent
from . step3_classes import Decimate
from ... list.utils import draw_list
from ... common_utils import apply_to_selected

#Panel
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
        data_path_low = "scene.Jet.list_low_res"
        data_path_high = "scene.Jet.list_high_res"
        draw_list(context, data_path_low, layout, "Low-res", tuple_buttons=(True, False, True, True))
        draw_list(context, data_path_high, layout, "High-res", tuple_buttons=(True, False, True, True))

        layout.operator("jet_apply_modifiers.btn", text="Apply Modifiers")
        layout.operator("jet_remove_parent.btn", text="Remove Parent")
        layout.operator("jet_assign_decimate.btn", text="Assign Decimate")
        layout.operator("jet_apply_decimate.btn", text="Apply Decimate")
        layout.operator("jet_add_sufix.btn", text="Add Sufix '_Low'").sufix = "_Low"
        layout.operator("jet_add_sufix.btn", text="Add Sufix '_High'").sufix = "_High"


#Operators
class VIEW3D_OT_jet_add_sufix(bpy.types.Operator):
    bl_idname = "jet_add_sufix.btn"
    bl_label = "Add sufix"
    bl_description = "Add sufix to the selected objects"

    sufix = bpy.props.StringProperty(name="sufix",default="_Low")

    def execute(self, context):
        for obj in context.selected_objects:
            if self.sufix in obj.name: continue
            obj.name = obj.name + self.sufix
        return {'FINISHED'}

class VIEW3D_OT_jet_assign_decimate(bpy.types.Operator):
    bl_idname = "jet_assign_decimate.btn"
    bl_label = "Assign Decimate"
    bl_description = "Assign Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        apply_to_selected(context, self.decimate.AssignDecimate)
        return {'FINISHED'}

class VIEW3D_OT_jet_apply_decimate(bpy.types.Operator):
    bl_idname = "jet_apply_decimate.btn"
    bl_label = "Apply Decimate"
    bl_description = "Apply Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        apply_to_selected(context, self.decimate.ApplyDecimate)
        return {'FINISHED'}

class VIEW3D_OT_jet_apply_modifiers(bpy.types.Operator):
    bl_idname = "jet_apply_modifiers.btn"
    bl_label = "Apply Modifiers"
    bl_description = "Apply modifiers to selected objects"

    def execute(self, context):
        apply_to_selected(context, apply_modifiers)
        return {'FINISHED'}

class VIEW3D_OT_jet_remove_parent(bpy.types.Operator):
    bl_idname = "jet_remove_parent.btn"
    bl_label = "Remove parents"
    bl_description = "Remove parent to selected objects"

    def execute(self, context):
        apply_to_selected(context, remove_parent)
        return {'FINISHED'}
