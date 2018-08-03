import bpy


#Panel
class VIEW3D_PT_jet_step2(bpy.types.Panel):
    bl_label = "Step 2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Optimization")

        col = layout.column(align=True)
        col.label("-Merge (Alt+M)")
        col.label("-Collapse (Alt+M)")
        col.label("-Dissolve Faces (F)")
        col.label("-Delete Vertex (X)")
        col.label("-Delete Vertex and Keep mesh (Ctrl+X)")
        col.label("-Delete Edge Loop (Ctrl+X)")


#Operators


