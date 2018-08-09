import bpy, sys
from . import bl_info

def get_id(object):
    if "id" not in object.keys():
        object["id"] = str(hash(object))
    return object["id"]

def select_obj_exclusive(obj, edit_mode = False):
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True
    if edit_mode: bpy.ops.object.mode_set(mode="EDIT")

def update_progress(job_title, progress, processingObj):
    length = 50
    block = int(round(length*progress))
    msg = "\r{0}: [{1:50s}] {2:3.2f}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress < 1:
        msg +=  " -> Obj: {0:50s}".format(processingObj)
    else:
        msg += "{0:50s}".format("")
        msg += ("\n" + job_title + " -> DONE\r\n")
    sys.stdout.write(msg)
    sys.stdout.flush()

def apply_to_selected(context, func, keep_selection = True, keep_active = True, value = None):
    sel_objs = context.selected_objects
    active_obj = context.active_object
    numObjs = len(sel_objs)
    if numObjs == 0: return None
    count = 1
    print("")
    for obj in sel_objs:
        try:
            func(obj) if value is None else func(obj, value)
        except:
            break

        update_progress(func.__name__, count / numObjs, obj.name)
        count = count + 1

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action='DESELECT')
    if keep_selection:
        for obj in reversed(sel_objs):
            obj.select = True
    if keep_active:
        if hasattr(bpy.context, "scene"):
            bpy.context.scene.objects.active = active_obj

def get_mesh_objs_selected(context):
    return [obj for obj in context.selected_objects if obj.type == 'MESH']

def any_mesh_obj_selected(context):
    return len(get_mesh_objs_selected(context)) > 0

def redraw(context):
    if hasattr(context, "area") and context.area is not None:
        context.area.tag_redraw()

def redraw():
    for area in bpy.context.screen.areas:
        if area.type in ['VIEW_3D']:
            area.tag_redraw()

def get_addon_name():
    return bl_info["name"]

def get_preferences():
    addon_name = get_addon_name()
    return bpy.context.user_preferences.addons[addon_name].preferences

def get_hotkey(context, keymap_item):
    wm = context.window_manager
    item = None
    #wm.keyconfigs.active.keymaps['Mesh'].keymap_items
    for km in wm.keyconfigs.user.keymaps:
        for kmi in km.keymap_items:
            if kmi.active and kmi.idname == keymap_item:
                item = kmi
                break

    if item is None:
        for km in wm.keyconfigs.addon.keymaps:
            for kmi in km.keymap_items:
                if kmi.active and kmi.idname == keymap_item:
                    item = kmi
                    break

    if item is None:
        for km in wm.keyconfigs.active.keymaps:
            for kmi in km.keymap_items:
                if kmi.active and kmi.idname == keymap_item:
                    item = kmi
                    break

    if item is None:
        return ""

    hotkey = ""
    if item.ctrl:
        hotkey = hotkey + "Ctrl+"
    if item.alt:
        hotkey = hotkey + "Alt+"
    if item.shift:
        hotkey = hotkey + "Shift+"
    if item.oskey:
        hotkey = hotkey + "OSkey+"
    if item.key_modifier != 'NONE':
        hotkey = hotkey + item.key_modifier + "+"

    return hotkey + item.type



