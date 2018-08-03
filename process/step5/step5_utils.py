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


def Append(blendfile, section='Object', link=False):
    #Check if the path and the file in blendfile exists
    section = '\\' + section + '\\'
    print(section)

    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        files = []
        for obj in data_from.objects:
            files.append({'name': obj})
        bpy.ops.wm.append(directory=blendfile + section, files=files, link=link)
