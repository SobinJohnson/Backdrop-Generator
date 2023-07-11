import bpy
from bpy.utils import register_class, unregister_class
from ..global_var import *

class del_scene(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.del_scene"
    bl_label = "Delete Scene" 
    bl_options = {"REGISTER", "UNDO"}       
    
    def execute(self,context):
        
        global instance_num
        objects_to_delete = []

        for obj in bpy.data.objects:
            if obj.name.startswith("bdg_"):
                objects_to_delete.append(obj)
        
        bpy.data.batch_remove(objects_to_delete)

        
        for material in bpy.data.materials:
            if material.name.startswith("bdg_"):
                bpy.data.materials.remove(material)
 
        #collection = bpy.data.collections.get("bdg_collection")
        for collection in bpy.data.collections:
            if collection.name.startswith("bdg_"):
                bpy.data.collections.remove(collection)
        
        if len(instance_obj_list)!=0:
            instance_obj_list.clear()
        
        instance_num=0
        
        return {'FINISHED'}
    
class del_obj(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.del_obj"
    bl_label = "Delete Objects" 
    bl_options = {"REGISTER", "UNDO"}       
    
    def execute(self,context):
        global instance_num
        
        objects_to_delete = []

        for obj in bpy.data.objects:
            if obj.name.startswith("bdg_instance_"+str(instance_num)):
                objects_to_delete.append(obj)
        
        bpy.data.batch_remove(objects_to_delete)
        
        if len(instance_obj_list)!=0:
            instance_obj_list.pop()    
        instance_num-=1
        
        return {'FINISHED'}

_classes = [
    del_scene,
    del_obj
    
]

def register():
    for c in _classes:
        register_class(c)

def unregister():
    for c in _classes:
        unregister_class(c)

