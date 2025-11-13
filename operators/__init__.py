# Operators Module

from .remesher import RemeshOperator
from .painter import PaintOperator
from .preview import PreviewOperator

# Register operators

def register():
    bpy.utils.register_class(RemeshOperator)
    bpy.utils.register_class(PaintOperator)
    bpy.utils.register_class(PreviewOperator)

# Unregister operators

def unregister():
    bpy.utils.unregister_class(RemeshOperator)
    bpy.utils.unregister_class(PaintOperator)
    bpy.utils.unregister_class(PreviewOperator)