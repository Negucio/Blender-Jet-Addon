import bpy
import bpy.ops
from bpy.app.handlers import load_post, persistent

#bpy.ops.wm.jet_modal_timer_op()

class JetModalTimerOp(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.jet_modal_timer_op"
    bl_label = "Jet Modal Timer Operator"

    _timer = None

    sel_objs = []

    def modal(self, context, event):
        if len(context.scene.Jet.list_low_res.obj_list)==0:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            if context.active_object != context.scene.Jet.active.object or \
                context.active_object.select != context.scene.Jet.active.select:
                if context.active_object.select:
                    objs_in_list = [o.object
                                    for o in context.scene.Jet.list_low_res.obj_list]
                    if context.active_object in objs_in_list:
                        idx = objs_in_list.index(context.active_object)
                        context.scene.Jet.list_low_res.obj_list_index_out = idx
                    context.scene.Jet.active.object = context.active_object
                context.scene.Jet.active.select = context.active_object.select

            #if context.scene.Jet.list_low_res.select_hi_rest_list:
            #    if self.sel_objs != context.selected_objects:
            #        print(str(self.sel_objs))
            #        sel_objs_in_list = [o.object
            #                        for o in context.scene.Jet.list_low_res.obj_list
            #                        if o.object in context.selected_objects]
            #        for obj in sel_objs_in_list:
            #            for hi_obj in obj.Jet.list_high_res.obj_list:
            #                hi_obj.object.select = True
            #
            #        self.sel_objs = context.selected_objects

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

@persistent
def jet_load_post(param):
    """
    Called on after loading a .blend file
    :param param: In order to append this function to the load_post handler, this has to receive a parameter.
    """
    ctx = bpy.context
    scn = ctx.scene
    scn.Jet.active.object = ctx.active_object
    scn.Jet.active.object.select = ctx.active_object.select

    if len(scn.Jet.list_low_res.obj_list)>0:
        bpy.ops.wm.jet_modal_timer_op()


def register():
    bpy.utils.register_class(JetModalTimerOp)

    if jet_load_post not in load_post:
        load_post.append(jet_load_post)


def unregister():
    bpy.utils.unregister_class(JetModalTimerOp)
    load_post.remove(jet_load_post)
