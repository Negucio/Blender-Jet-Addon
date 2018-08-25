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

class SnapPropertyGroup(bpy.types.PropertyGroup):
    def get_snap(self, type):
        ts = bpy.context.scene.tool_settings
        ret = True
        if type == 'FACE':
            ret = ret and ts.snap_element == type
            ret = ret and ts.use_snap_project
            ret = ret and ts.use_snap_align_rotation
            ret = ret and not ts.use_snap_self
        if type == 'VERTEX':
            ret = ret and ts.snap_element == type
            ret = ret and not ts.use_snap_align_rotation
            ret = ret and not ts.use_snap_self

        return ret

    def set_snap(self, value, type):
        ts = bpy.context.scene.tool_settings
        if type == 'FACE':
            ts.snap_element = type
            ts.use_snap_project = True
            ts.use_snap_align_rotation = True
            ts.use_snap_self = False
        if type == 'VERTEX':
            ts.snap_element = type
            ts.use_snap_align_rotation = False
            ts.use_snap_self = False

    vertex = bpy.props.BoolProperty(default=False,
                                    description="Align rotation = False\nSnap onto itself = True",
                                    get=lambda self: self.get_snap('VERTEX'),
                                    set=lambda self, value: self.set_snap(value, 'VERTEX'))
    face = bpy.props.BoolProperty(default=False,
                                  description="Project individual elements = True\nAlign rotation = True\nSnap onto itself = False",
                                  get=lambda self: self.get_snap('FACE'),
                                  set=lambda self, value: self.set_snap(value, 'FACE'))

class ScnJetPropertyGroup(bpy.types.PropertyGroup):
    list_low_res = bpy.props.PointerProperty(type=ObjListPropertyGroup)

    high_res_file = bpy.props.StringProperty(name="", default="", subtype="FILE_PATH")
    optimized_res_file = bpy.props.StringProperty(name="", default="", subtype="FILE_PATH")

    opt_high_objs = bpy.props.CollectionProperty(type=ObjectPropertyGroup)
    opt_meshes = bpy.props.CollectionProperty(type=MeshPropertyGroup)
    high_meshes = bpy.props.CollectionProperty(type=MeshPropertyGroup)

    high_res = bpy.props.BoolProperty(options={'HIDDEN'}, default=False)

    tag = bpy.props.PointerProperty(type=TagEdgePropertyGroup)

    autosmooth = bpy.props.IntProperty(default=180, max=180, min=0)

    snap = bpy.props.PointerProperty(type=SnapPropertyGroup)


class ObjJetPropertyGroup(bpy.types.PropertyGroup):
    object_id = property(get_id)
    list_high_res = bpy.props.PointerProperty(type=ObjListPropertyGroup)

    opt_mesh = bpy.props.PointerProperty(type=bpy.types.Mesh)
    high_mesh = bpy.props.PointerProperty(type=bpy.types.Mesh)


def register():
    bpy.utils.register_class(SnapPropertyGroup)
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
    bpy.utils.unregister_class(SnapPropertyGroup)


