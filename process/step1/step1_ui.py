import bpy

#Panel
class VIEW3D_PT_jet_step1(bpy.types.Panel):
    bl_label = "Step 1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

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
        layout.label("Retopology:")

        col = layout.column(align=True)
        col.label("-Activar Snap a caras para retopo")
        col.label("-Activar Snap a vértices para soldar vértices rápidamente")
        col.operator("object.shade_flat", text="Flat")
        col.label("*Integración con Addon Ice Tools (para Shrinkwrap)")
        self.ice_tools(col, context)
        col.label("-Opciones de visualización (hidden wire, x-ray… posiblemente usar lo mismo que Ice Tools)")
        col.label("-Crear y Extruír vértices (Ctrl+Click)")
        col.label("-Rellenar (F)")
        col.label("-LoopCut and Slide (Ctrl+R)")
        col.label("-Knife (K)")
        col.label("-Activar addon F2 (Recordatorio)")
        col.label("-Extender Vértices (Alt+D)")
        col.label("-Rip (V)")
        col.label("-Rip Fill (Alt+V)")


#Operators








