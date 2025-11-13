import bpy

class SimplePanel(bpy.types.Panel):
    bl_label = "Quad Remesher"
    bl_idname = "OBJECT_PT_quad_remesher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Remesh"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Settings:")
        col.prop(context.scene, 'remesh_setting1')  # Example property
        col.operator('object.quad_remesher_operator')

def register():
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimplePanel)

if __name__ == "__main__":
    register()