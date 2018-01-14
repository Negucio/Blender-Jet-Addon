import bpy
from .. common_utils import SelectObjectExclusive

class Decimate():
    def __init__(self):
        self.decimateName = 'decimate_Jet'

    def AssignDecimate(self, obj):
        if obj == None or obj.type != "MESH": return None
        SelectObjectExclusive(obj)

        if len([m for m in obj.modifiers if m.name == self.decimateName]) == 0:
            dec = obj.modifiers.new(self.decimateName, 'DECIMATE')
            # Collapse
            dec.decimate_type = 'COLLAPSE'
            dec.ratio = 0.1

            # Un-Subdivide
            # dec.decimate_type = 'UNSUBDIV'
            # dec.iterations = 2

            # Planar
            # dec.decimate_type = 'DISSOLVE'
            # dec.angle_limit = 1.309     #75 grados en radianes

    def ApplyDecimate(self, obj):
        if obj == None or obj.type != "MESH": return None
        SelectObjectExclusive(obj)

        for mod in obj.modifiers:
            if mod.type == 'DECIMATE' and mod.name == self.decimateName:
                bpy.ops.object.modifier_apply(modifier=mod.name)