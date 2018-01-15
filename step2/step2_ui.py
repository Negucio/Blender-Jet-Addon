import bpy
from .. common_utils import ApplyToSelected
from . step2_utils import triangulate, is_texture_atlas_enabled, enable_texture_atlas

class VIEW3D_OT_jet_triangulate(bpy.types.Operator):
    bl_idname = "jet_triangulate.btn"
    bl_label = "Triangulate"
    bl_description = "Triangulate"

    def execute(self, context):
        ApplyToSelected(context, triangulate)
        return {'FINISHED'}


class VIEW3D_OT_jet_texture_atlas_on(bpy.types.Operator):
    bl_idname = "jet_texture_atlas_on.btn"
    bl_label = "EnableTextureAtlas"
    bl_description = "Enable Texture Atlas Addon"

    def execute(self, context):
        enable_texture_atlas()
        return {'FINISHED'}


class VIEW3D_PT_jet_step2(bpy.types.Panel):
    bl_label = "Step 2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"

    @classmethod
    def poll(cls, context):
        return True

    def texture_atlas(self, layout):
        if not is_texture_atlas_enabled():
            layout.label("Texture Atlas is not enabled", icon="ERROR")
            layout.operator("jet_texture_atlas_on.btn", text="Enable Texture Atlas")
        else:
            layout.operator("scene.ms_add_lightmap_group", text="Start Texture Atlas").name = "TextureAtlas_Jet"
            layout.operator("object.ms_run", text="Start Manual Unwrap")
            layout.operator("uv.average_islands_scale", text="Average Islands Scale")
            layout.operator("uv.pack_islands", text="Pack Islands")
            layout.label("Shotpacker??")
            layout.operator("object.ms_run_remove", text="Finish Manual Unwrap")

    def draw(self, context):
        layout = self.layout
        layout.label("UVs completas")

        self.texture_atlas(layout)

        layout.operator("jet_triangulate.btn", text="Triangulate")
