import bpy
import os.path
from .step5_utils import apply_modifiers, remove_parent, append, assign_subsurf, \
    apply_transform_constraints, set_decimate_geometry
from ... common_utils import apply_to_selected

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

#Panel
class VIEW3D_PT_jet_step5(bpy.types.Panel):
    bl_label = "5. Model Preparation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene.Jet.info, "model_preparation", text="", icon="INFO")

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Jet, "subdivisions", text="Subbdivisions")
        row.operator("jet_assign_subsurf.btn", text="", icon="RIGHTARROW").subdiv = context.scene.Jet.subdivisions

        col = layout.column(align=True)
        col.operator("jet_apply_modifiers.btn", text="Apply Modifiers")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Jet, "decimate_ratio", text="Decimate Ratio")
        row.operator("jet_assign_decimate.btn", text="", icon="RIGHTARROW").ratio = context.scene.Jet.decimate_ratio

        col = layout.column(align=True)
        col.operator("jet_apply_transf_constraints.btn", text="Apply Transf & Constraints")
        col = layout.column(align=True)
        col.operator("jet_remove_parent.btn", text="Remove Parent")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Jet, "optimized_res_file", text="Proxy")
        row.operator("load_blend.btn", text="", icon="FILESEL").attr = "optimized_res_file"
        row = col.row(align=True)
        row.prop(context.scene.Jet, "high_res_file", text="Hi-Res")
        row.operator("load_blend.btn", text="", icon="FILESEL").attr = "high_res_file"

        hi =    (context.scene.Jet.high_res_file != "") and os.path.isfile(context.scene.Jet.high_res_file)
        proxy = (context.scene.Jet.optimized_res_file != "") and os.path.isfile(context.scene.Jet.optimized_res_file)
        row = col.row()
        row.enabled = hi and proxy
        op = col.operator("jet_append_opt_high.btn", text="Bring models to scene")
        op.optimized = context.scene.Jet.optimized_res_file
        op.high = context.scene.Jet.high_res_file

        #col.operator("jet_switch_hi_opt.btn", text="Swap Optimized / High Resolution")
        row = layout.row(align=True)
        row.enabled = hi and proxy
        row.prop(context.scene.Jet.swap, "model", expand=True)


#Operators
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
        append(context, self.optimized, self.high)
        context.scene.Jet.swap.model = 'proxy'
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

class VIEW3D_OT_jet_set_decimate(bpy.types.Operator):
    bl_idname = "jet_assign_decimate.btn"
    bl_label = "Assign decimate"
    bl_description = "Assign decimate and/or set the ratio in all selected objects"

    ratio = bpy.props.IntProperty(default=10)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        apply_to_selected(context, set_decimate_geometry, value=self.ratio/100)
        return {'FINISHED'}


class VIEW3D_OT_jet_assign_subsurf(bpy.types.Operator):
    bl_idname = "jet_assign_subsurf.btn"
    bl_label = "Assign subsurf"
    bl_description = "Assign subsurf and/or set the subdivisions in all selected objects"

    subdiv = bpy.props.IntProperty(default=2)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        apply_to_selected(context, assign_subsurf, value=self.subdiv)
        return {'FINISHED'}


class VIEW3D_OT_jet_apply_transf_constraints(bpy.types.Operator):
    bl_idname = "jet_apply_transf_constraints.btn"
    bl_label = "Apply Transform and Constraints"
    bl_description = "Apply Transform and Constraints in all selected objects"

    def execute(self, context):
        apply_to_selected(context, apply_transform_constraints)
        return {'FINISHED'}


class VIEW3D_OT_jet_load_blend_file(Operator, ImportHelper):
    bl_idname = "load_blend.btn"
    bl_label = "Load blend dialog"

    filename_ext = ".blend"

    filter_glob = StringProperty(
            default="*.blend",
            options={'HIDDEN'},
            maxlen=255)

    attr = StringProperty(default="",
                          options={'HIDDEN'})

    def execute(self, context):
        setattr(context.scene.Jet, self.attr, self.filepath)
        return {'FINISHED'}

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