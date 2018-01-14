import bpy, bmesh
from ..common_utils import SelectObjectExclusive

def EnableAndConfigAutosmooth(obj):
    if obj == None or obj.type != "MESH": return None
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 3.14159    #180 degrees (pi radians)


def ManageSharp(context, mark=True):
    obj = context.active_object
    if obj is None or \
       obj.type != "MESH" or \
       obj.mode != 'EDIT':
        return None

    me = obj.data
    me.show_edge_sharp = True
    bm = bmesh.from_edit_mesh(me)  # Save the mesh of the object in the variable to work with it by code
    bm.edges.ensure_lookup_table()  # It's advisable calling this method in order to work with the different components of an object (verts, edges or faces) using bmesh
    for e in bm.edges:
        if e.select:  # If the edge is selected
            e.smooth = not mark  # Set edge as Seam
    bmesh.update_edit_mesh(me, False)

def ManageSeam(context, mark=True):
    obj = context.active_object
    if obj is None or \
       obj.type != "MESH" or \
       obj.mode != 'EDIT':
        return None

    me = obj.data
    me.show_edge_seams = True
    bm = bmesh.from_edit_mesh(me)  # Save the mesh of the object in the variable to work with it by code
    bm.edges.ensure_lookup_table()  # It's advisable calling this method in order to work with the different components of an object (verts, edges or faces) using bmesh
    for e in bm.edges:
        if e.select:  # If the edge is selected
            e.seam = mark
    bmesh.update_edit_mesh(me, False)

# Function for mark Sharp edges as Seams working directly with the object data (vertices, edges and faces).
# Requires Object mode to work properly
def SharpToSeam(obj):
    if obj == None or obj.type != "MESH": return None
    SelectObjectExclusive(obj)
    for e in obj.data.edges:
        if e.use_edge_sharp:
            # e.use_edge_sharp = False   #Set edge as Not Sharp - "Clear Sharp" in this edge
            e.use_seam = True  # Set edge as Seam

    obj.data.show_edge_seams = True  # It's necessary to call this function in order to display the edge as Seams (red color)


# Function for mark Sharp edges as Seams using BMesh library to work with the object data (vertices, edges and faces).
# Requires Edit mode to work properly
def SharpToSeamBMesh(obj):
    if obj == None or obj.type != "MESH": return None
    SelectObjectExclusive(obj, edit_mode=True)  # Select only this object and set "Edit Mode"
    me = obj.data
    bm = bmesh.from_edit_mesh(me)  # Save the mesh of the object in the variable to work with it by code
    bm.edges.ensure_lookup_table()  # It's advisable calling this method in order to work with the different components of an object (verts, edges or faces) using bmesh
    for e in bm.edges:
        if not e.smooth:  # If the edge is Sharp, aka Not Smooth
            # e.smooth = True    #Set edge as Not Sharp, aka Smooth - "Clear Sharp" in this edge
            e.seam = True  # Set edge as Seam
    bmesh.update_edit_mesh(me, False)
    bpy.ops.object.mode_set(mode="OBJECT")  # Set "Object Mode"

    obj.data.show_edge_seams = True  # It's necessary to call this function in order to display the edge as Seams (red color)

def Unwrap(obj):
    if obj == None or obj.type != "MESH": return None
    SelectObjectExclusive(obj, edit_mode=True)  # Select only this object and set "Edit Mode"
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.mode_set(mode="OBJECT")




