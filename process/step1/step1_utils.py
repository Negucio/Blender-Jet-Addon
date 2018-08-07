
def SnapToFaces(scene):
    scene.tool_settings.snap_element = 'FACE'
    scene.tool_settings.use_snap_project = True
    scene.tool_settings.use_snap_align_rotation = True
    scene.tool_settings.use_snap_self = False

def SnapToVertices(scene):
    scene.tool_settings.snap_element = 'VERTEX'
    scene.tool_settings.use_snap_self = False
    scene.tool_settings.use_snap_align_rotation = False
    scene.tool_settings.use_snap_self = True









