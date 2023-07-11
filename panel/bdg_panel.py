
import bpy
from bpy.utils import register_class, unregister_class
from ..global_var import *


class bdg_props(bpy.types.PropertyGroup):
    
    
    instance_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        description="Pick an object to scatter behind your subject",
        name="Object"
    )
        
    is_obj: bpy.props.BoolProperty(
        name= "Object",
        description="Select whether you want to scatter objects behind your subject",
        default=True)
        
        
    is_plat: bpy.props.BoolProperty(
        name= "Platform",
        description="Select whether you want a platform for your subject",
        default=True)
        
    options_type =   [
                ("UNIFORM", "Uniform", "Generate uniform pattern"),
                ("RANDOM", "Random", "Generate random pattern")
                ]
                
    type: bpy.props.EnumProperty(
    items=options_type,
    name="Type",
    description="Select the scatter distribution type"
    )
    
    plat_color: bpy.props.FloatVectorProperty(
        name="Platform Color",
        subtype="COLOR",
        description="Select a color for the platform",
        size=4,
        default=(0.019, 0.095, 0.242,1),
        min=0.0,
        max=1.0
    )
    
    
    bg_color: bpy.props.FloatVectorProperty(
        name="Background Color",
        subtype="COLOR",
        description="Select a color for the background",
        size=4,
        default=(1, 0.94, 0.83,1),
        min=0.0,
        max=1.0
    )
    
    plat_rad: bpy.props.FloatProperty(
        name="Platform radius",
        description="Set the desired platform radius",
        default=0.5,
        min=0,
        max=5
    )
    scale_randomness: bpy.props.FloatProperty(
        name="Scale randomness",
        description="Set how large you want the size deviation to be.\n\nA 0 value makes all the objects same size as the orginally instanced object",
        default=0.4,
        min=0,
        max=1
    )
    
    rot_randomness: bpy.props.FloatProperty(
        name="Rotation randomness",
        description="Set how much you want the rotaion to deviate from original.\n\nA 0 value all the objects have same rotation as the orginally instanced object",
        default=0.5,
        min=0,
        max=1
    )
    
    def uni_update(self,context):
        loc_uni=self.loc_uni
        count=self.count
        offset=self.offset
        so=bpy.data.objects.get("bdg_instance_"+str(instance_num)+"_uniform")
        so.location=(loc_uni[0],loc_uni[1],loc_uni[2])
        so.modifiers["Array"].relative_offset_displace[0] = offset[0]
        #so.modifiers["Array.001"].relative_offset_displace[0] = 0
        so.modifiers["Array.001"].relative_offset_displace[2] = offset[1]
        so.modifiers["Array"].count = count[0]
        so.modifiers["Array.001"].count = count[1]
     
    loc_uni: bpy.props.FloatVectorProperty(
        name="Coordinate",
        subtype='XYZ',
        description="Set the position for the objects",
        default=(-1,1,0.25),
        update=uni_update
    )
       
    count: bpy.props.IntVectorProperty(
        name="Count",
        size=2,
        description="Set number of objects in x-axiz and z-axiz",
        default=(10,15),
        min=0,
        update=uni_update
    )
    
    offset: bpy.props.FloatVectorProperty(
        name="Offset",
        size=2,
        description="Set offset of objects in x-axiz and z-axiz",
        default=(1.2,1.2),
        min=0,
        update=uni_update
    )
    
    
    spread_x: bpy.props.FloatProperty(
        name="Spread-X",
        description="Set how far you want the objects to spread along x-axiz",
        default=1,
        min=0,
    )
    spread_z: bpy.props.FloatProperty(
        name="Spread-Z",
        description="Set how far you want the objects to spread along x-axiz",
        default=1,
        min=0,
    )
    
    p_rot_speed: bpy.props.FloatProperty(
        name="Platform Rotation Speed",
        description="Set the rotation speed of the platform",
        default=1,
    )
    
    obj_rot_speed: bpy.props.FloatProperty(
        name="Object Rotation Speed",
        description="Set the rotation speed of the platform",
        default=0.5,
        min=0
    )
    
    obj_speed: bpy.props.FloatProperty(
        name="Object Speed",
        default=1,
        description="Set the rotation speed of the platform",
        min=0
    )
    
    num: bpy.props.IntProperty(
        name="Amount",
        description="Set the nnumber of objects to scatter",
        default=15,
        min=0
    )
        
    is_anim: bpy.props.BoolProperty(
        name= "Animated",
        description="Select whether you want the back drop to be animated",
        default=True)
        
    def update_intensity(self,context):
        intensity=self.l_intensity
        light=bpy.data.objects.get("bdg_light_point")
        light.data.energy=intensity*1500
        light=bpy.data.objects.get("bdg_light_bg_1")
        light.data.energy=intensity*6000
        light=bpy.data.objects.get("bdg_light_bg_2")
        light.data.energy=intensity*75000
        light=bpy.data.objects.get("bdg_light_bg_3")
        light.data.energy=intensity*200000
        light=bpy.data.objects.get("bdg_light_a")
        light.data.energy=intensity*150
                
        
    l_intensity: bpy.props.FloatProperty(
        name="Light Intensity",
        description="Set the intensity of all the lights in the scene.",
        default=1.2,
        update=update_intensity,
        min=0,
        max=10
        
    )    
            
    is_front: bpy.props.BoolProperty(
        name= "Allow objects in front",
        description="Select whether you want objects in front of ur subject.",
        default=False)
    
    def update_seed(self,context) :
        
        all_objects = bpy.data.objects
        for obj in all_objects:
            if obj.name.startswith("bdg_instance_"+str(instance_num)):
                bpy.data.objects.remove(obj, do_unlink=True)
        backdrop_gen.scatter_obj(bpy.context)
        all_objects = bpy.data.objects
        collection = bpy.data.collections.get("bdg_collection")
        if collection == None :
            collection = bpy.data.collections.new("bdg_collection")

        bdg_objects = []

        for obj in all_objects:
            if obj.name.startswith("bdg_instance"):
                bdg_objects.append(obj)
        
        for obj in bdg_objects:
            if obj.name in bpy.context.collection.objects:
                bpy.context.collection.objects.unlink(obj)
            if obj.name not in collection.objects:
                collection.objects.link(obj)
        bpy.context.scene.frame_set(0)  
               
    
    seed_num: bpy.props.IntProperty(
        name="Seed",
        description="Set the  seed value to get various random iterations",
        default=0,
        min=0,
        update=update_seed
    )
    
        
register_class(bdg_props)
bpy.types.Scene.bdg_props = bpy.props.PointerProperty(type=bdg_props)   

class bdg_panel(bpy.types.Panel):
    #Creates a Panel in the Object properties window
    bl_label = "Backdrop Generator"
    bl_idname = "BDG_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Backdrop Generator"
        
    def draw(self, context):
        
        obj = context.object
        layout = self.layout
        props=bpy.context.scene.bdg_props
        
        row = layout.row()
        row.prop(props,"is_obj")
        #row.prop(props,"is_ball")
        row.prop(props,"is_plat")
        row = layout.row()
        if props.is_obj:
            row.prop(props,"instance_obj")
            row = layout.row()
            row.prop(props,"type")
            row = layout.row()
        if props.is_plat:
            row.prop(props,"plat_rad")
            row = layout.row()
        if props.is_obj:    
            if props.type=="UNIFORM":
                row = layout.row()
                row.prop(props,"loc_uni")
                row = layout.row()
                row.prop(props,"count")
                row = layout.row()
                row.prop(props,"offset")
                row = layout.row()
            if props.type=="RANDOM":
                row.prop(props,"num")
                row = layout.row()
                row.prop(props,"spread_x")
                row.prop(props,"spread_z")
                row = layout.row()
                row.prop(props,"seed_num")
                row = layout.row()
                row.prop(props,"is_front")
                row = layout.row()
        row.prop(props,"bg_color")
        row = layout.row()
        if props.is_plat:
            row.prop(props,"plat_color")
        row = layout.row()
        row.prop(props,"l_intensity")
        row = layout.row()
        row.prop(props,"is_anim")
        if props.is_obj or props.is_plat:
            if props.is_anim:
                if props.type=="RANDOM":
                    if props.is_obj :
                        row = layout.row()
                        row.prop(props,"obj_speed")
                        row.prop(props,"obj_rot_speed")
                        row = layout.row()
                        row.prop(props,"rot_randomness")
                        row.prop(props,"scale_randomness")
                row = layout.row()
                if props.is_plat: 
                    row.prop(props,"p_rot_speed")
        row = layout.row()
        row.operator("object.backdrop_gen")
        if props.is_obj:
            row = layout.row()
            row.operator("object.obj_scatter")
            row.operator("object.del_obj")
        row = layout.row()
        row.operator("object.del_scene")
        
_classes = [
    bdg_panel
]

def register():
    for c in _classes:
        register_class(c)

def unregister():
    for c in _classes:
        unregister_class(c)
