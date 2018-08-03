import bpy

#Panel
class VIEW3D_PT_jet_step6(bpy.types.Panel):
    bl_label = "Step 6"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label("Bake Sets Creation")


#Operators

