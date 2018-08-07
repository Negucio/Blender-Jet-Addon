import bpy
import os.path
from . step5_utils import apply_modifiers, remove_parent, AppendMeshes, AppendObjects, Switch
from ... list.utils import draw_list
from ... common_utils import apply_to_selected
from . step5_classes import Decimate

#Panel
class VIEW3D_PT_jet_step5(bpy.types.Panel):
    bl_label = "Step 5"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Model Preparation")

        data_path_low = "scene.Jet.list_low_res"
        draw_list(context, data_path_low, layout, "Low-res", tuple_buttons=(True, False, True, True))
        if len(context.scene.Jet.list_low_res.obj_list) > 0:
            idx = context.scene.Jet.list_low_res.obj_list_index
            data_path_high = "scene.Jet.list_low_res.obj_list[" + str(idx) + "].object.Jet.list_high_res"
            draw_list(context, data_path_high, layout, "High-res", tuple_buttons=(True, False, True, True))

        col = layout.column(align=True)
        col.label("-Limitar subdivisiones")
        col.operator("jet_apply_decimate.btn", text="Apply Decimate")
        col.label("- % Decimate")

        col.operator("jet_apply_modifiers.btn", text="Apply Modifiers")
        col.label("-Aplicar restricciones y transformación visual")
        col.operator("jet_remove_parent.btn", text="Remove Parent")

        col = layout.column(align=True)
        col.prop(context.scene.Jet, "optimized_res_file", text="Optimized")
        col.prop(context.scene.Jet, "high_res_file", text="Hi-Res")

        op = col.operator("jet_append_opt_high.btn", text="Append")
        op.optimized = context.scene.Jet.optimized_res_file
        op.high = context.scene.Jet.high_res_file

        col.operator("jet_switch_hi_opt.btn", text="Swap Optimized / High Resolution")


#Operators
#col.operator("jet_add_sufix.btn", text="Add Sufix '_Low'").sufix = "_Low"
#col.operator("jet_add_sufix.btn", text="Add Sufix '_High'").sufix = "_High"
#class VIEW3D_OT_jet_add_sufix(bpy.types.Operator):
#    bl_idname = "jet_add_sufix.btn"
#    bl_label = "Add sufix"
#    bl_description = "Add sufix to the selected objects"
#
#    sufix = bpy.props.StringProperty(name="sufix",default="_Low")
#
#    def execute(self, context):
#        for obj in context.selected_objects:
#            if self.sufix in obj.name: continue
#            obj.name = obj.name + self.sufix
#        return {'FINISHED'}

class VIEW3D_OT_jet_append_opt_high(bpy.types.Operator):
    bl_idname = "jet_append_opt_high.btn"
    bl_label = ""
    bl_description = ""

    optimized = bpy.props.StringProperty(default='')
    high = bpy.props.StringProperty(default='')

    @classmethod
    def poll(cls, context):
        hi = (context.scene.Jet.high_res_file != "") and os.path.isfile(context.scene.Jet.high_res_file)
        return hi and ((context.scene.Jet.optimized_res_file != "") and os.path.isfile(context.scene.Jet.optimized_res_file))

    def execute(self, context):
        AppendMeshes(self.optimized, collection=context.scene.Jet.opt_meshes, link=True)
        AppendObjects(self.optimized, collection=context.scene.Jet.opt_high_objs, link=False)

        AppendMeshes(self.high, collection=context.scene.Jet.high_meshes, link=True)

        for o in context.scene.Jet.opt_high_objs:
            o.object.Jet.opt_mesh.mesh = o.object.data
            for m in context.scene.Jet.high_meshes:
                if o.object.data.name == m.mesh.name:
                    o.object.Jet.high_mesh.mesh = m.mesh

        return {'FINISHED'}



class VIEW3D_OT_jet_switch_hi_opt(bpy.types.Operator):
    bl_idname = "jet_switch_hi_opt.btn"
    bl_label = ""
    bl_description = ""

    @classmethod
    def poll(cls, context):
        return len(context.scene.Jet.opt_high_objs)>0

    def execute(self, context):
        context.scene.Jet.high_res = not context.scene.Jet.high_res
        Switch(context.scene.Jet.opt_high_objs, context.scene.Jet.high_res)
        return {'FINISHED'}


class VIEW3D_OT_jet_apply_modifiers(bpy.types.Operator):
    bl_idname = "jet_apply_modifiers.btn"
    bl_label = "Apply Modifiers"
    bl_description = "Apply modifiers to selected objects"

    def execute(self, context):
        apply_to_selected(context, apply_modifiers)
        return {'FINISHED'}


class VIEW3D_OT_jet_remove_parent(bpy.types.Operator):
    bl_idname = "jet_remove_parent.btn"
    bl_label = "Remove parents"
    bl_description = "Remove parent to selected objects"

    def execute(self, context):
        apply_to_selected(context, remove_parent)
        return {'FINISHED'}


class VIEW3D_OT_jet_assign_decimate(bpy.types.Operator):
    bl_idname = "jet_assign_decimate.btn"
    bl_label = "Assign Decimate"
    bl_description = "Assign Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        apply_to_selected(context, self.decimate.AssignDecimate)
        return {'FINISHED'}


class VIEW3D_OT_jet_apply_decimate(bpy.types.Operator):
    bl_idname = "jet_apply_decimate.btn"
    bl_label = "Apply Decimate"
    bl_description = "Apply Decimate modifier to selected objects"

    decimate = Decimate()

    def execute(self, context):
        apply_to_selected(context, self.decimate.ApplyDecimate)
        return {'FINISHED'}
