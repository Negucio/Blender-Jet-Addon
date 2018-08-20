import bpy
from ... common_utils import get_hotkey
from . step1_utils import SnapToFaces, SnapToVertices

#Panel
class VIEW3D_PT_jet_step1(bpy.types.Panel):
    bl_label = "1. Retopology"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def ice_tools(self, layout, context):
        box = layout.box()
        row_sw = box.row(align=True)
        row_sw.alignment = 'EXPAND'
        row_sw.operator("setup.retopo", "Set Up Retopo Mesh")
        row_sw = box.row(align=True)
        row_sw.alignment = 'EXPAND'
        row_sw.operator("shrink.update", "Shrinkwrap Update")

        row_fv = box.row(align=True)
        row_fv.alignment = 'EXPAND'
        row_fv.operator("freeze_verts.retopo", "Freeze")
        row_fv.operator("thaw_freeze_verts.retopo", "Thaw")
        row_fv.operator("show_freeze_verts.retopo", "Show")

        if context.active_object is not None:
            row_view = box.row(align=True)
            row_view.alignment = 'EXPAND'
            row_view.prop(context.object, "show_wire", toggle =False)
            row_view.prop(context.object, "show_x_ray", toggle =False)
            row_view.prop(context.space_data, "show_occlude_wire", toggle =False)

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label("Snap to:")
        row.operator("jet_snap_faces.btn", text="Face")
        row.operator("jet_snap_vertices.btn", text="Vertex")

        col = layout.column(align=True)
        col.operator("object.shade_flat", text="Flat")

        col = layout.column(align=True)
        self.ice_tools(col, context)

        col = layout.column(align=True)
        col.operator("mesh.dupli_extrude_cursor", text="Extrude to Mouse - " + get_hotkey(context, "mesh.dupli_extrude_cursor"))
        col.operator("mesh.f2", text="MakeEdge/Face - " + get_hotkey(context, "mesh.f2"))
        col.operator("mesh.loopcut_slide", text="LoopCut and Slide - " + get_hotkey(context, "mesh.loopcut_slide"))
        col.operator("mesh.knife_tool", text="Knife - " + get_hotkey(context, "mesh.knife_tool"))
        col.operator("mesh.rip_edge_move", text="Extend Vertices - " + get_hotkey(context, "mesh.rip_edge_move"))
        col.operator("mesh.rip_move", text="Rip - " + get_hotkey(context, "mesh.rip_move"))
        col.operator("mesh.rip_move_fill", text="Rip Fill - " + get_hotkey(context, "mesh.rip_move_fill"))

#Operators
class VIEW3D_OT_jet_snap_faces(bpy.types.Operator):
    bl_idname = "jet_snap_faces.btn"
    bl_label = "Snap to face"
    bl_description = "Project individual elements = True\nAlign rotation = True\nSnap onto itself = False"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        SnapToFaces(context.scene)
        return {'FINISHED'}

class VIEW3D_OT_jet_snap_vertices(bpy.types.Operator):
    bl_idname = "jet_snap_vertices.btn"
    bl_label = "Snap to vertex"
    bl_description = "Align rotation = False\nSnap onto itself = True"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        SnapToVertices(context.scene)
        return {'FINISHED'}







