import bpy
from ... list.utils import draw_list

#Panel
class VIEW3D_PT_jet_step6(bpy.types.Panel):
    bl_label = "6. Bake Sets Creation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Jet"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

        data_path_low = "scene.Jet.list_low_res"
        draw_list(context, data_path_low, layout, "Low-res", tuple_buttons=(True, False, True, True))
        if len(context.scene.Jet.list_low_res.obj_list) > 0:
            idx = context.scene.Jet.list_low_res.obj_list_index
            data_path_high = "scene.Jet.list_low_res.obj_list[" + str(idx) + "].object.Jet.list_high_res"
            draw_list(context, data_path_high, layout, "High-res", tuple_buttons=(True, False, True, True))


#Operators

