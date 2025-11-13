bl_info = {
    "name": "Blender Quad Remesher",
    "blender": (2, 82, 0),  # Minimum Blender version
    "category": "3D View",
}

import bpy

def register():
    # Registering UI Panels
    from . import panels
    panels.register()


def unregister():
    # Unregistering UI Panels
    from . import panels
    panels.unregister()

if __name__ == "__main__":
    register()