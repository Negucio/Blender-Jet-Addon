import bpy


class ObjIdPropertyGroup(bpy.types.PropertyGroup):
    id = bpy.props.StringProperty(name="id", default="Id")
    object = bpy.props.StringProperty(name="object name", default="Object")


class ObjListPropertyGroup(bpy.types.PropertyGroup):
    high_obj_list_idx = bpy.props.IntProperty(name="Index", default=0, min=0)
    high_obj_list = bpy.props.CollectionProperty(type=ObjIdPropertyGroup)
    low_obj_list_idx = bpy.props.IntProperty(name="Index", default=0, min=0)
    low_obj_list = bpy.props.CollectionProperty(type=ObjIdPropertyGroup)


class ScnJetPropertyGroup(bpy.types.PropertyGroup):
    ui = bpy.props.PointerProperty(options={'HIDDEN'}, type=ObjListPropertyGroup)


class ObjJetPropertyGroup(bpy.types.PropertyGroup):
    high_res = bpy.props.BoolProperty(options={'HIDDEN'}, default = False)
    low_res = bpy.props.BoolProperty(options={'HIDDEN'}, default = False)


def register():
    bpy.utils.register_class(ObjIdPropertyGroup)
    bpy.utils.register_class(ObjListPropertyGroup)
    bpy.utils.register_class(ObjJetPropertyGroup)
    bpy.utils.register_class(ScnJetPropertyGroup)

    bpy.types.Scene.Jet = bpy.props.PointerProperty(options={'HIDDEN'}, type=ScnJetPropertyGroup)
    bpy.types.Object.Jet = bpy.props.PointerProperty(options={'HIDDEN'}, type=ObjJetPropertyGroup)

def unregister():
    del bpy.types.Scene.Jet

    bpy.utils.unregister_class(ScnJetPropertyGroup)
    bpy.utils.unregister_class(ObjJetPropertyGroup)
    bpy.utils.unregister_class(ObjListPropertyGroup)
    bpy.utils.unregister_class(ObjIdPropertyGroup)


