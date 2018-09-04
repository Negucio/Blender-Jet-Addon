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
                                  description="Project individual elements = True\nAlign rotation = True\nSnap onto itself = False",
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

    #TODO: Model preparation text is too long for the tooltip character limit
    #TODO: Search some way to circumvent that limitation or remove all these variables
    #retopology_text = "The first stop once we have our high resolution model ready is to generate a lower resolution model that resembles the high resolution shape. This process is known as “Retopology” or “Retopo”, and it consists on creating a new topology (geometry surface) on top of the high resolution model." + \
    #            "\n\nThere are many specific techniques, tricks, tools… but the main 3 ways in which you’ll generate the new mesh are:" + \
    #            "\n  1. Reusing the high resolution model: taking subdivisions away and deleting unnecessary geometry (like support loops), decimating (in the case of a sculpt without subdivisions, for example) or merging elements." + \
    #            "\n  2. Using the snap tools to model while the new mesh is automatically projected on the original (very common and especially useful with organic models." + \
    #            "\n  3. Modeling on top of the original shape to create similar shapes (but keeping the control that snapping takes away - useful for hard-surface models)."
    #
    #optimization_text = "When working for videogames, you usually have to work within a 'polygon budget'. For the game to run smoothly, the number of polygons of each prop and character have to be limited." + \
    #                    "\n\nOptimization is the part of the process in which you take the model from retopo, and 'clean' it so the number of polygons ends up within the limit." + \
    #                    "\n\nIt's usually measured in triangles, as it's the minimum number of sides that a polygon can have, and this way you have a more reliable number to work with."
    #
    #smooth_sharp_text = "After you have the final geometry for your model, it's time to define how that geometry looks like. To do that, we use Smoothing and Sharpening." + \
    #                    "\n\nBasically, you'd have to define which parts of the geometry are smooth, and then choose which edges would be sharp (corners)." + \
    #                    "\n\nThe steps to follow we suggest to perform this part of the process are:" + \
    #                    "\n  1. Smoothing everything." + \
    #                    "\n  2. Set autosmooth as enabled and setting it to 180 degrees (this will make your model completely smooth, while showing the desired edges as sharp)." + \
    #                    "\n  3. Marking desired edges a sharp."
    #
    #uvs_text = "UVs are the XYZ equivalents in a 2D plane. It’s the internal distribution of faces in two dimensions, which allows you to define how a texture will be projected onto the 3D Surface." + \
    #            "\n\nThis process is referred to as “unwrapping”, because it usually requires to mark “seams”, and then unfold (unwrap) the mesh to achieve a flat version of the model. This doesn’t affect the 3D shape, it happens in a paralell 2D view." + \
    #            "\n\nOne of the keys of UVs when working for games is that edges marked as sharp also have to be seams, so this addon offers you an option to quickly convert all sharp edges into seams automatically." + \
    #            "\n\nAfter that, you have to refine and add seams wherever needed (typically in hidden areas and corners, to avoid having “cuts” in the texture when it’s projected on the model), and continue with the unwrapping process." + \
    #            "\n\nThe last part of making good UVs is the “packing”: taking all of the UVs and placing them in the UV Editor making the best use of the space available."
    #
    #model_prep_text = "Before we proceed to the next steps, it’s necessary that you prepare your models. One of the challenges at this point is dealing with very high resolution models; they make the scene sluggish and the files big." + \
    #                    "\n\nThis addon makes it easy and efficient: you only have to create two separate .blend files, each of them containing a different version of the model that will be linked to the final file. This way loading times to open the files and working with the model will be much faster, and your high resolution model only needs to be stored in a single heavy file, instead of being present in every version of the final model you save." + \
    #                    "\n\nLet’s check the steps to follow:" + \
    #                    "\n  1. Create a .blend file and import your high resolution model." + \
    #                    "\n  2. Apply all modifiers to avoid issues later on." + \
    #                    "\n  3. Save the file and make a copy: this will be an optimized version of your high resolution model (proxy)." + \
    #                    "\n  5. From this addon, you will define the .blend files assigned to the high resolution and proxy models." + \
    #                    "\n  6. You can now click on “Bring models to the scene” and you’ll be set up with the proxy version of your model." + \
    #                    "\n  7. Now you can move, rotate, scale, or parent the objects of the proxy model, as it’s quicker and less heavy. At any time you can just swap the proxy with the high resolution model and viceversa. This is useful to link low resolution model (the final one that goes to the videogame) with high resolution model before exploding it and performing the bakes." + \
    #                    "\n\nIMPORTANT NOTE: To be able to swap the proxy and high resolution models, all of the objects need to keep their original names, otherwise they won’t work."
    #
    #bake_sets_creation_text = "This is the last step of the model preparation process. Basically, you must link sets of high resolution models to the low resolution models they “belong” to." + \
    #                           "\n\nA bake is the extraction of the high resolution mesh details to the low resolution mesh in the form of a texture." + \
    #                           "\n\nThese bake sets will define which high resolution objects are baked in which low resolution objects, which will make it easy to explode the model. Explode? Yes: model exploding is basically taking groups of pieces apart so the bakes from one piece don’t affect the adjacent ones."

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
        description="Press to display information about Retopology process",
        update=lambda self, context: self.update(context, "retopology"))
    optimization = bpy.props.BoolProperty(default=False,
        description="Press to display information about Optimization process",
        update=lambda self, context: self.update(context, "optimization"))
    smoothing_sharpening = bpy.props.BoolProperty(default=False,
        description="Press to display information about Smoothing & Sharpening process",
        update=lambda self, context: self.update(context, "smoothing_sharpening"))
    uvs = bpy.props.BoolProperty(default=False,
        description="Press to display information about UV Mapping process",
        update=lambda self, context: self.update(context, "uvs"))
    model_preparation = bpy.props.BoolProperty(default=False,
        description="Press to display information about Model Preparation process",
        update=lambda self, context: self.update(context, "model_preparation"))
    bake_sets_creation = bpy.props.BoolProperty(default=False,
        description="Press to display information about Bake Sets Creation process",
        update=lambda self, context: self.update(context, "bake_sets_creation"))

#Scene
class ScnJetPropertyGroup(bpy.types.PropertyGroup):
    list_low_res = bpy.props.PointerProperty(type=LowObjListPropertyGroup)

    high_res_file = bpy.props.StringProperty(name="", default="", subtype="FILE_PATH")
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


