import bpy
from ... common_utils import get_hotkey

#Panel
class VIEW3D_PT_jet_step2(bpy.types.Panel):
    bl_label = "Step 2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Optimization")

        col = layout.column(align=True)
        col.operator("mesh.merge", text="Merge - " + get_hotkey(context, "mesh.merge"))
        #col.operator("mesh.merge", text="Merge - " + get_hotkey(context, "mesh.merge")).type = "COLLAPSE"
        col.operator("jet_merge.btn", text="Collapse - " + get_hotkey(context, "mesh.merge")).type = "COLLAPSE"
        col.operator("mesh.f2", text="Dissolve Faces - " + get_hotkey(context, "mesh.f2"))

        col.operator("jet_delete_menu.btn", text="Delete Vertex - " + "X")
        op = col.operator("mesh.dissolve_mode", text="Delete Vertex and keep mesh - " + get_hotkey(context, "mesh.dissolve_mode"))
        op.use_verts=True
        op.use_face_split = False
        op.use_boundary_tear = False
        op = col.operator("mesh.dissolve_mode", text="Delete Edge Loop - " + get_hotkey(context, "mesh.dissolve_mode"))
        op.use_verts=True
        op.use_face_split = False
        op.use_boundary_tear = False

#Operators
class VIEW3D_OT_jet_merge(bpy.types.Operator):
    bl_idname = "jet_merge.btn"
    bl_label = ""
    bl_description = ""

    type = bpy.props.StringProperty(default="COLLAPSE")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        bpy.ops.mesh.merge(type=self.type)
        return {'FINISHED'}

class VIEW3D_OT_jet_delete_menu(bpy.types.Operator):
    bl_idname = "jet_delete_menu.btn"
    bl_label = ""
    bl_description = ""

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        bpy.ops.wm.call_menu(name="VIEW3D_MT_edit_mesh_delete")
        return {'FINISHED'}
