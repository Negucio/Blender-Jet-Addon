
bl_info = {
    "name": "Jet",
    "author": "",
    "description": "",
    "version": (0, 2, 0),
    "blender": (2, 7, 8),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}

import bpy
from . import data, ui, handler

def register():
    ui.register()
    data.register()
    handler.register()


def unregister():
    handler.unregister()
    data.unregister()
    ui.unregister()
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()

