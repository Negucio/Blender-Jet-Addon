import bpy
from bpy.props import StringProperty, CollectionProperty, IntProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, Object
from .. common_utils import select_obj_exclusive

class ObjPropertyGroup(PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    object = PointerProperty(name="object", type=Object)

class LowObjListPropertyGroup(PropertyGroup):
    """
    Stores the properties of the low-res UIList item
    """
    from_out = BoolProperty(default=False)

    def select_hi_res_list(self, obj):
        for hi_ob in obj.Jet.list_high_res.obj_list:
            hi_ob.object.select = True

    # When the outside updating property is set,
    # a flag is defined to distinguish from the inside updating property
    def set_out(self, value):
        self.from_out = True
        self.obj_list_index = value
        self.from_out = False

    def get(self):
        return self.obj_list_index

    def update(self, context):
        if len(self.obj_list) == 0:
            return
        bpy.ops.wm.jet_modal_timer_op()
        obj = self.obj_list[self.obj_list_index].object
        # Select the object
        # Different behaviour depending on where the variable has been updated from
        if self.from_out: obj.select = True
        else: select_obj_exclusive(obj)
        #Make the object Active
        context.scene.objects.active = obj

        #Select the linked hi-res list
        if context.scene.Jet.list_low_res.select_hi_rest_list:
            self.select_hi_res_list(obj)

    obj_list = CollectionProperty(type=ObjPropertyGroup)
    obj_list_index = IntProperty(name="Index", default=0, min=0, update=update)
    select_hi_rest_list = BoolProperty(default=True)

    # This property allows different behaviours when updating from outside or from inside
    obj_list_index_out = IntProperty(name="Index", default=0, min=0, set=set_out)


class HiObjListPropertyGroup(PropertyGroup):
    """
    Stores the properties of the hi-res UIList item
    """
    def update(self, context):
        if len(self.obj_list) == 0:
            return
        obj = self.obj_list[self.obj_list_index].object
        #Select the object
        obj.select = True
        #Make the object Active
        context.scene.objects.active = obj

    obj_list = CollectionProperty(type=ObjPropertyGroup)
    obj_list_index = IntProperty(name="Index", default=0, min=0, update=update)
