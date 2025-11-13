bl_info = {
    "name": "Quad Remesher",
    "blender": (2, 92, 0),
    "category": "Mesh",
}

import bpy

class QuadRemesherPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Example of addon preferences
    resolution: bpy.props.IntProperty(
        name="Resolution",
        description="Set the quad resolution",
        default=1,
        min=1,
        max=5,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Quad Remesher Preferences")
        layout.prop(self, "resolution")
        
def register():
    bpy.utils.register_class(QuadRemesherPreferences)

def unregister():
    bpy.utils.unregister_class(QuadRemesherPreferences)

if __name__ == "__main__":
    register()