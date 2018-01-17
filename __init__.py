
bl_info = {
    "name": "Jet",
    "author": "",
    "description": "",
    "version": (0, 0, 0),
    "blender": (2, 7, 8),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}

import bpy
from . import data, ui

def register():
    ui.register()
    data.register()


def unregister():
    data.unregister()
    ui.unregister()
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()

