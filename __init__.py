bl_info = {
    "name": "Backdrop Generator",
    "author": "Sobin Johnson",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "A backdrop generating tool to create a plesing backdrop and lighting for your product render",
    "category": "Object",
}

from . import bdg_source

modules = [
    bdg_source
]


def register():
    for module in modules:
        module.register()
        
def unregister():

    for module in modules:
        module.unregister()