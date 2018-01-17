import bpy
from ... common_utils import apply_to_selected
from . step3_classes import Decimate
from ... list.list_ui import Resolution

#Panel
class VIEW3D_PT_jet_step3(bpy.types.Panel):
    bl_label = "Step 3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def add_obj_list(self, context, layout, resolution):
        if resolution == Resolution.Low:
            obj_list_ui = "DATA_UL_jet_low_obj_list"
            obj_list = "low_obj_list"
            obj_list_idx = "low_obj_list_idx"
        elif resolution == Resolution.High:
            obj_list_ui = "DATA_UL_jet_high_obj_list"
            obj_list = "high_obj_list"
            obj_list_idx = "high_obj_list_idx"

        box = layout.box()
        row = box.row()
        row.label(text=resolution.name + ":")
        row.prop(context.scene.Jet.ui, obj_list)
        row = box.row()
        row.template_list(obj_list_ui, "", context.scene.Jet.ui, obj_list, context.scene.Jet.ui, obj_list_idx)
        row = box.row(align=True)
        row.operator("jet_obj_list_add.btn", text="Add").resolution = obj_list
        row.operator("jet_obj_list_remove.btn", text="Remove").resolution = obj_list
        #row = box.row(align=True)
        #row.operator("jet_obj_Blist_add.btn", text="Select")
        #row.operator("jet_obj_list_remove.btn", text="Deselect")

    def draw(self, context):
        layout = self.layout
        layout.label("Hi-res Model Prep")
        self.add_obj_list(context, layout, Resolution.High)
        self.add_obj_list(context, layout, Resolution.Low)
        layout.operator("assign_decimate.btn", text="Assign Decimate")
        layout.operator("apply_decimate.btn", text="Apply Decimate")
        layout.operator("add_sufix.btn", text="Add Sufix '_Low'").sufix = "_Low"
        layout.operator("add_sufix.btn", text="Add Sufix '_High'").sufix = "_High"


#Operators
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
        apply_to_selected(context, self.decimate.AssignDecimate)
        return {'FINISHED'}

class VIEW3D_OT_jet_apply_decimate(bpy.types.Operator):
    bl_idname = "apply_decimate.btn"
    bl_label = "Apply Decimate"
    bl_description = "Apply Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        apply_to_selected(context, self.decimate.ApplyDecimate)
        return {'FINISHED'}

