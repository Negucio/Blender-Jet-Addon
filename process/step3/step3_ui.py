import bpy

from ... list.list_classes import List, Resolution
from ... common_utils import apply_to_selected
from . step3_classes import Decimate

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
        sel_btn = col.operator("jet_obj_list_select_all.btn", text="Select All")
        sel_btn.resolution = list.resolution.name
        sel_btn.select = True
        col = row.column()
        desel_btn = col.operator("jet_obj_list_select_all.btn", text="Deselect All")
        desel_btn.resolution = list.resolution.name
        desel_btn.select = False

    def add_obj_list(self, context, layout, list):
        if type(list) is not List: return None
        box = layout.box()
        row = box.row()
        row.label(text=list.resolution.name + ":")
        row.prop(context.scene.Jet.ui, list.obj_list)
        row = box.row()
        row.template_list(list.data_ul_obj_list, "", context.scene.Jet.ui, list.obj_list, context.scene.Jet.ui, list.obj_list_idx)

        self.add_buttons(context, box, list)


    def draw(self, context):
        layout = self.layout
        layout.label("Hi-res Model Prep")
        self.add_obj_list(context, layout, self.list_low)
        self.add_obj_list(context, layout, self.list_high)
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

