import bpy, os
from ... common_utils import select_obj_exclusive

def apply_modifiers(obj):
    if not hasattr(obj, "modifiers"): return None
    select_obj_exclusive(obj)
    for mod in obj.modifiers:
        try:
            bpy.ops.object.modifier_apply(modifier = mod.name)
        except: #If the modifier is disabled can not be applied and Blender throws an error
            continue

def remove_parent(obj):
    if not hasattr(obj, "parent"): return None
    obj.parent = None


def AppendMeshes(blendfile, collection=None, link=False, fake_user=False):
    section = '\\' + 'Mesh' + '\\'
    imported = []

    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        files = []
        for mesh in data_from.meshes:
            files.append({'name': mesh})
            imported.append(mesh)
        bpy.ops.wm.append(directory=blendfile + section, files=files, link=link, set_fake=True)

    for m in bpy.data.meshes:
        cond = m.name in imported
        if link:
            cond = cond and (blendfile == m.library.filepath)
        if cond:
            if fake_user:
                m.use_fake_user = True
            if collection is not None:
                item = collection.add()
                item.mesh = m

def AppendObjects(blendfile, collection=None, link=False, fake_user=False):
    section = '\\' + 'Object' + '\\'
    imported = []

    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        files = []
        for obj in data_from.objects:
            files.append({'name': obj})
            imported.append(obj)
        bpy.ops.wm.append(directory=blendfile + section, files=files, link=link, set_fake=True)

    for o in bpy.data.objects:
        cond = o.name in imported
        if link:
            cond = cond and (blendfile == o.library.filepath)
        if cond:
            if fake_user:
                o.use_fake_user = True
            if collection is not None:
                item = collection.add()
                item.object = o


def Switch(objs, high):
    for o in objs:
        if high:
            o.object.data = o.object.Jet.high_mesh.mesh
        else:
            o.object.data = o.object.Jet.opt_mesh.mesh