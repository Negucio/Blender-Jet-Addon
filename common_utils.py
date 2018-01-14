import bpy, sys

def SelectObjectExclusive(obj, edit_mode = False):
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

def ApplyToSelected(context, func):
    sel_objs = context.selected_objects
    active_obj = context.active_object
    numObjs = len(sel_objs)
    if numObjs == 0: return None
    count = 1
    print("")
    for obj in sel_objs:
        try:
            func(obj)
        except:
            break

        update_progress(func.__name__, count / numObjs, obj.name)
        count = count + 1

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action='DESELECT')
    for obj in reversed(sel_objs):
        obj.select = True
    if hasattr(bpy.context, "scene"):
        bpy.context.scene.objects.active = active_obj

