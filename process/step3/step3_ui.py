import bpy

from . step3_utils import apply_modifiers, remove_parent
from . step3_classes import Decimate
from ... list.list_classes import List, Resolution
from ... common_utils import apply_to_selected

#Panel
class VIEW3D_PT_jet_step3(bpy.types.Panel):
    bl_label = "Step 3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    list_high = List(Resolution.High, "high_obj_list", "high_obj_list_idx", "DATA_UL_jet_high_obj_list")
    list_low = List(Resolution.Low, "low_obj_list", "low_obj_list_idx", "DATA_UL_jet_low_obj_list")

    @classmethod
    def poll(cls, context):
        return True

    def add_buttons(self, context, layout, list):
        row = layout.row(align=True)
        col = row.column()
        add_btn = col.operator("jet_obj_list_add.btn", text="Add")
        add_btn.resolution = list.resolution.name
        add_btn.obj_list = list.obj_list
        col = row.column()
        obj_list = getattr(context.scene.Jet.ui, list.obj_list)
        col.enabled = (len(obj_list) > 0)
        rmv_btn = col.operator("jet_obj_list_remove.btn", text="Remove")
        rmv_btn.resolution = list.resolution.name
        rmv_btn.obj_list = list.obj_list
        rmv_btn.obj_list_idx = list.obj_list_idx

        row = layout.row(align=True)
        row.enabled = (len(obj_list) > 0)
        col = row.column()
        sel_btn = col.operator("jet_obj_list_selection.btn", text="Select All")
        sel_btn.resolution = list.resolution.name
        sel_btn.select = True
        col = row.column()
        desel_btn = col.operator("jet_obj_list_selection.btn", text="Deselect All")
        desel_btn.resolution = list.resolution.name
        desel_btn.select = False

        row = layout.row(align=True)
        row.enabled = (len(obj_list) > 0)
        col = row.column()
        show_btn = col.operator("jet_obj_list_visibility.btn", text="Show All")
        show_btn.resolution = list.resolution.name
        show_btn.hide = False
        col = row.column()
        hide_btn = col.operator("jet_obj_list_visibility.btn", text="Hide All")
        hide_btn.resolution = list.resolution.name
        hide_btn.hide = True

    def add_obj_list(self, context, layout, list):
        if type(list) is not List: return None
        box = layout.box()
        row = box.row()
        row.label(text=list.resolution.name + ":")
        row.prop(context.scene.Jet.ui, list.obj_list)
        row = box.row()
        row.template_list(list.data_ul_obj_list, "", context.scene.Jet.ui, list.obj_list, context.scene.Jet.ui, list.obj_list_idx)
        self.add_buttons(context, box, list)
        return box


    def draw(self, context):
        layout = self.layout
        layout.label("Hi-res Model Prep")
        self.add_obj_list(context, layout, self.list_low)
        self.add_obj_list(context, layout, self.list_high)

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
