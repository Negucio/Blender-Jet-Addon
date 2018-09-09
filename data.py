import bpy
import os
from . common_utils import get_id
from . list.data import HiObjListPropertyGroup, LowObjListPropertyGroup
from . draw import Draw

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
                                  description="Project individual elements = True\n" + \
                                              "Align rotation = True\n" + \
                                              "Snap onto itself = False",
                                  get=lambda self: self.get_snap('FACE'),
                                  set=lambda self, value: self.set_snap(value, 'FACE'))

class SwapPropertyGroup(bpy.types.PropertyGroup):
    def swap(self, objs, high):
        for o in objs:
            if high:
                o.object.data = o.object.Jet.high_mesh
            else:
                o.object.data = o.object.Jet.opt_mesh

    def update_model(self, context):
        j = context.scene.Jet
        j.high_res = (j.swap.model=='hi')
        self.swap(j.opt_high_objs, j.high_res)

    model = bpy.props.EnumProperty(default='proxy', items=[
                                    ('proxy', 'Proxy', 'Proxy'),
                                    ('hi', 'Hi-Res', 'Hi-Res')],
                                   update=lambda self, context: self.update_model(context))

class InfoPropertyGroup(bpy.types.PropertyGroup):
    drawing = Draw()
    do_update = bpy.props.BoolProperty(default=True)

    retopology_text = "After you have a high resolution model, you need to create a lower resolution one that mimics its shape." \
                "\n\nYou do this by creating a new topology that adapts to the high resolution model's shape using snapping tools, " \
                "\nand this process is called 'Retopology' or 'Retopo'." \
                "\n\n(Press the button for more info.)"

    optimization_text = "When working for videogames, you usually have a 'polygon budget'." \
                        "\n\nIn the optimization process you'll take the model resulting from 'Retopo', and reduce polygons " \
                        "\nas necessary until you have the appropriate number of polygons." \
                        "\n\n(Press the button for more info.)"

    smooth_sharp_text = "Not all edges are equal, and especially when you're dealing with low resolution models, smoothing " \
                        "\ncan create some weird gradients in the surface." \
                        "\n\nTo avoid that, the sharpest corners of your model should be marked as sharp." \
                        "\n\n(Press the button for more info.)"

    uvs_text = "This is the part of the process in which you have to define how textures will be projected onto your model. " \
               "\n\nIn order to do that, you must unwrap and unfold it so you can turn a 2D image into a 3D model later." \
               "\n\n(Press the button for more info.)"

    model_prep_text = "Once you have your high and low resolution models, you'll need to bake the details from the high " \
                      "\nresolution onto the low resolution's UVs. " \
                      "\n\nBut before you set everything up, it's a good idea to prepare your models for easing the next stage " \
                      "\n(especially if you're working with extremely high polygon models). " \
                      "\n\n(Press the button for more info.)"

    bake_sets_creation_text = "Each low resolution object typically encompasses several smaller high resolution models." \
                              "\n\nCreate bake sets to assign a series of high resolution objects to a low resolution one," \
                              "\nand then you'll be able to control them easily during the bake setup." \
                              "\n\n(Press the button for more info.)"

    def reset_others(self, origin):
        self.do_update = False
        if origin!="retopology":
            self.retopology = False
        if origin != "optimization":
            self.optimization = False
        if origin != "smoothing_sharpening":
            self.smoothing_sharpening = False
        if origin != "uvs":
            self.uvs = False
        if origin != "model_preparation":
            self.model_preparation = False
        if origin != "bake_sets_creation":
            self.bake_sets_creation = False
        self.do_update = True

    def get_text(self, origin):
        loc = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "info"))
        file = open(os.path.join(loc, origin), 'r')
        return file.read()

    def update(self, context, origin):
        if not self.do_update:
            return

        self.reset_others(origin)

        value = getattr(self, origin)
        if value:
            self.drawing.hide_info(context)
            text = self.get_text(origin)
            self.drawing.display_info(context, text)
        else:
            self.drawing.hide_info(context)

    retopology = bpy.props.BoolProperty(default=False,
        description=retopology_text,
        update=lambda self, context: self.update(context, "retopology"))
    optimization = bpy.props.BoolProperty(default=False,
        description=optimization_text,
        update=lambda self, context: self.update(context, "optimization"))
    smoothing_sharpening = bpy.props.BoolProperty(default=False,
        description=smooth_sharp_text,
        update=lambda self, context: self.update(context, "smoothing_sharpening"))
    uvs = bpy.props.BoolProperty(default=False,
        description=uvs_text,
        update=lambda self, context: self.update(context, "uvs"))
    model_preparation = bpy.props.BoolProperty(default=False,
        description=model_prep_text,
        update=lambda self, context: self.update(context, "model_preparation"))
    bake_sets_creation = bpy.props.BoolProperty(default=False,
        description=bake_sets_creation_text,
        update=lambda self, context: self.update(context, "bake_sets_creation"))

#Scene
class ScnJetPropertyGroup(bpy.types.PropertyGroup):
    list_low_res = bpy.props.PointerProperty(type=LowObjListPropertyGroup)

    high_res_file = bpy.props.StringProperty(name="", default="")
    optimized_res_file = bpy.props.StringProperty(name="", default="", subtype="FILE_PATH")

    opt_high_objs = bpy.props.CollectionProperty(type=ObjectPropertyGroup)
    opt_meshes = bpy.props.CollectionProperty(type=MeshPropertyGroup)
    high_meshes = bpy.props.CollectionProperty(type=MeshPropertyGroup)

    high_res = bpy.props.BoolProperty(options={'HIDDEN'}, default=False)

    tag = bpy.props.PointerProperty(type=TagEdgePropertyGroup)

    autosmooth = bpy.props.IntProperty(default=180, max=180, min=0)

    decimate_ratio = bpy.props.IntProperty(default=10, max=100, min=0)

    subdivisions = bpy.props.IntProperty(default=2, max=10, min=0)

    snap = bpy.props.PointerProperty(type=SnapPropertyGroup)

    swap = bpy.props.PointerProperty(type=SwapPropertyGroup)

    info = bpy.props.PointerProperty(type=InfoPropertyGroup)

#Object
class ObjJetPropertyGroup(bpy.types.PropertyGroup):
    list_high_res = bpy.props.PointerProperty(type=HiObjListPropertyGroup)

    opt_mesh = bpy.props.PointerProperty(type=bpy.types.Mesh)
    high_mesh = bpy.props.PointerProperty(type=bpy.types.Mesh)

def register():
    bpy.utils.register_class(SnapPropertyGroup)
    bpy.utils.register_class(InfoPropertyGroup)
    bpy.utils.register_class(SwapPropertyGroup)
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
    bpy.utils.unregister_class(SwapPropertyGroup)
    bpy.utils.unregister_class(InfoPropertyGroup)
    bpy.utils.unregister_class(SnapPropertyGroup)


