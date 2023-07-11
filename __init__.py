bl_info = {
    "name": "Backdrop Generator",
    "author": "Sobin Johnson",
    "version": (1, 0),
    "blender": (3, 41, 0),
    "location": "View3D",
    "description": "A backdrop generating tool to create a plesing backdrop and lighting for your product render",
    "category": "Object",
}

from . import scatter,panel

modules = (
    scatter,
    panel
)


def register():
    for module in modules:
        module.register()
        
def unregister():

    for module in modules:
        module.unregister()