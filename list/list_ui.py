import bpy
from .. common_utils import any_mesh_obj_selected
from . list_classes import Resolution

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
    obj_list = bpy.props.StringProperty(default='')

    def add_obj_toList(self, context, object, obj_list):
        item = obj_list.add()
        item.id = object.Jet.object_id
        item.object = object.name
        object.Jet.high_res = (self.resolution == Resolution.High.name)
        object.Jet.low_res = (self.resolution == Resolution.Low.name)

    def is_obj_suitable(self, ids, obj):
        if obj.type != 'MESH': return False
        if obj.Jet.object_id in ids: return False
        if self.resolution == Resolution.High.name and obj.Jet.low_res: return False
        if self.resolution == Resolution.Low.name and obj.Jet.high_res: return False
        return True

    @classmethod
    def poll(cls, context):
        return any_mesh_obj_selected(context)

    def execute(self, context):
        obj_list = getattr(context.scene.Jet.ui, self.obj_list)
        ids = [o.id for o in obj_list]
        for obj in context.selected_objects:
            if not self.is_obj_suitable(ids, obj): continue
            self.add_obj_toList(context, obj, obj_list)
        return {'FINISHED'}


class DATA_OT_jet_obj_list_remove(bpy.types.Operator):
    bl_idname = "jet_obj_list_remove.btn"
    bl_label = "Remove Object"
    bl_description = "Remove object from the list"

    resolution = bpy.props.StringProperty(default='')
    obj_list = bpy.props.StringProperty(default='')
    obj_list_idx = bpy.props.StringProperty(default='')

    @classmethod
    def poll(cls, context):
        #This check needs to be done in the panel
        #Local variable 'obj_list' can not be accessed from this class method
        return True

    def execute(self, context):
        obj_list_idx = getattr(context.scene.Jet.ui, self.obj_list_idx)
        obj_list = getattr(context.scene.Jet.ui, self.obj_list)
        obj = [o for o in context.scene.objects if o.Jet.object_id == obj_list[obj_list_idx].id][0]
        obj_list.remove(obj_list_idx)
        obj.Jet.high_res = False
        obj.Jet.low_res = False
        return {'FINISHED'}


class DATA_OT_jet_obj_list_select_all(bpy.types.Operator):
    bl_idname = "jet_obj_list_select_all.btn"
    bl_label = "Select all objects"
    bl_description = "Select all objects from the list"

    select = bpy.props.BoolProperty(default=True)
    resolution = bpy.props.StringProperty(default='')

    @classmethod
    def poll(cls, context):
        #This check needs to be done in the panel
        #Local variable 'obj_list' can not be accessed from this class method
        return True

    def execute(self, context):
        for obj in context.scene.objects:
            if (obj.Jet.low_res and self.resolution == Resolution.Low.name) or \
               (obj.Jet.high_res and self.resolution == Resolution.High.name):
                obj.select = self.select
        return {'FINISHED'}




