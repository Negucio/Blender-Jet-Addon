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
    def select_hi_res_list(self, obj):
        for hi_ob in obj.Jet.list_high_res.obj_list:
            hi_ob.object.select = True

    def update(self, context):
        obj = self.obj_list[self.obj_list_index].object
        #Select the object
        select_obj_exclusive(obj)
        #Make the object Active
        context.scene.objects.active = obj
        #Select the linked hi-res list
        self.select_hi_res_list(obj)

    obj_list = CollectionProperty(type=ObjPropertyGroup)
    obj_list_index = IntProperty(name="Index", default=0, min=0, update=update)


class HiObjListPropertyGroup(PropertyGroup):
    """
    Stores the properties of the hi-res UIList item
    """
    def update(self, context):
        obj = self.obj_list[self.obj_list_index].object
        #Select the object
        select_obj_exclusive(obj)
        #Make the object Active
        context.scene.objects.active = obj

    obj_list = CollectionProperty(type=ObjPropertyGroup)
    obj_list_index = IntProperty(name="Index", default=0, min=0, update=update)
