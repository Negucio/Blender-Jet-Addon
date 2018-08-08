import bpy
from . common_utils import get_id
from . list.data import ObjListPropertyGroup


class ObjIdPropertyGroup(bpy.types.PropertyGroup):
    id = bpy.props.StringProperty(name="id", default="Id")
    object = bpy.props.StringProperty(name="object name", default="Object")

class MeshPropertyGroup(bpy.types.PropertyGroup):
    mesh = bpy.props.PointerProperty(name="mesh", type=bpy.types.Mesh)

class ObjectPropertyGroup(bpy.types.PropertyGroup):
    object = bpy.props.PointerProperty(name="object", type=bpy.types.Object)

class TagEdgePropertyGroup(bpy.types.PropertyGroup):
    def get_tag(self, type):
        return bpy.context.scene.tool_settings.edge_path_mode == type

    def set_tag(self, value, type):
        bpy.context.scene.tool_settings.edge_path_mode = (type if value else 'SELECT')

    sharp = bpy.props.BoolProperty(default=False,
                                   get=lambda self: self.get_tag('SHARP'),
                                   set=lambda self, value: self.set_tag(value, 'SHARP'))
    seam = bpy.props.BoolProperty(default=False,
                                   get=lambda self: self.get_tag('SEAM'),
                                   set=lambda self, value: self.set_tag(value, 'SEAM'))

class ScnJetPropertyGroup(bpy.types.PropertyGroup):
    list_low_res = bpy.props.PointerProperty(type=ObjListPropertyGroup)

    high_res_file = bpy.props.StringProperty(name="", default="", subtype="FILE_PATH")
    optimized_res_file = bpy.props.StringProperty(name="", default="", subtype="FILE_PATH")

    opt_high_objs = bpy.props.CollectionProperty(type=ObjectPropertyGroup)
    opt_meshes = bpy.props.CollectionProperty(type=MeshPropertyGroup)
    high_meshes = bpy.props.CollectionProperty(type=MeshPropertyGroup)

    high_res = bpy.props.BoolProperty(options={'HIDDEN'}, default=False)

    tag = bpy.props.PointerProperty(type=TagEdgePropertyGroup)


class ObjJetPropertyGroup(bpy.types.PropertyGroup):
    object_id = property(get_id)
    list_high_res = bpy.props.PointerProperty(type=ObjListPropertyGroup)

    opt_mesh = bpy.props.PointerProperty(type=bpy.types.Mesh)
    high_mesh = bpy.props.PointerProperty(type=bpy.types.Mesh)


def register():
    bpy.utils.register_class(TagEdgePropertyGroup)
    bpy.utils.register_class(MeshPropertyGroup)
    bpy.utils.register_class(ObjectPropertyGroup)
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
    bpy.utils.unregister_class(MeshPropertyGroup)
    bpy.utils.unregister_class(ObjectPropertyGroup)
    bpy.utils.unregister_class(TagEdgePropertyGroup)


