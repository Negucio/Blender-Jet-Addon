import bpy
from . common_utils import get_id
from . list.data import ObjListPropertyGroup


class ObjIdPropertyGroup(bpy.types.PropertyGroup):
    id = bpy.props.StringProperty(name="id", default="Id")
    object = bpy.props.StringProperty(name="object name", default="Object")


class ScnJetPropertyGroup(bpy.types.PropertyGroup):
    list_low_res = bpy.props.PointerProperty(type=ObjListPropertyGroup)


class ObjJetPropertyGroup(bpy.types.PropertyGroup):
    object_id = property(get_id)
    list_high_res = bpy.props.PointerProperty(type=ObjListPropertyGroup)
    high_res = bpy.props.BoolProperty(options={'HIDDEN'}, default = False)
    low_res = bpy.props.BoolProperty(options={'HIDDEN'}, default = False)


def register():
    bpy.utils.register_class(ObjIdPropertyGroup)
    bpy.utils.register_class(ObjJetPropertyGroup)
    bpy.utils.register_class(ScnJetPropertyGroup)

    bpy.types.Scene.Jet = bpy.props.PointerProperty(options={'HIDDEN'}, type=ScnJetPropertyGroup)
    bpy.types.Object.Jet = bpy.props.PointerProperty(options={'HIDDEN'}, type=ObjJetPropertyGroup)


def unregister():
    del bpy.types.Scene.Jet
    del bpy.types.Object.Jet

    bpy.utils.unregister_class(ScnJetPropertyGroup)
    bpy.utils.unregister_class(ObjJetPropertyGroup)
    bpy.utils.unregister_class(ObjIdPropertyGroup)


