import bpy
from .. common_utils import any_mesh_obj_selected
from . list_utils import get_id
from enum import IntEnum

#Enum
class Resolution(IntEnum):
    Low = 0
    High = 1

#List
class DATA_UL_jet_high_obj_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        layout.label(item.object)

class DATA_UL_jet_low_obj_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        layout.label(item.object)

#Operators
class DATA_OT_jet_obj_list_add(bpy.types.Operator):
    bl_idname = "jet_obj_list_add.btn"
    bl_label = "Add Object"
    bl_description = "Add object to the list"

    resolution = bpy.props.StringProperty(default='')

    def add_obj_toList(self, context, object, obj_list):
        item = obj_list.add()
        item.id = get_id(object)
        item.object = object.name
        object.Jet.high_res = (self.resolution == 1)
        object.Jet.low_res = (self.resolution == 0)

    @classmethod
    def poll(cls, context):
        return any_mesh_obj_selected(context)

    def execute(self, context):
        obj_list = getattr(context.scene.Jet.ui, self.resolution)
        ids = [o.id for o in obj_list]
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            if get_id(obj) in ids: continue
            self.add_obj_toList(context, obj, obj_list)
        return {'FINISHED'}


class DATA_OT_jet_obj_list_remove(bpy.types.Operator):
    bl_idname = "jet_obj_list_remove.btn"
    bl_label = "Remove Object"
    bl_description = "Remove object from the list"

    resolution = bpy.props.StringProperty(default='')

    @classmethod
    def poll(cls, context):
        #TODO: must check if the list contains objets
        return True #len(context.scene.Jet.ui.obj_List) > 0

    def execute(self, context):
        index = context.scene.Jet.ui.obj_List_Index
        context.scene.Jet.ui.obj_List.remove(index)
        return {'FINISHED'}


class DATA_OT_jet_obj_list_select_all(bpy.types.Operator):
    bl_idname = "jet_obj_list_select_all.btn"
    bl_label = "Select all objects"
    bl_description = "Select all objects from the list"

    @classmethod
    def poll(cls, context):
        return True #len(context.scene.Jet.ui.obj_List) > 0

    def execute(self, context):

        return {'FINISHED'}


