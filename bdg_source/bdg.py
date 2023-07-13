bl_info = {
    "name": "Backdrop Generator",
    "author": "Sobin Johnson",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy
import math
import random
from bpy.utils import register_class, unregister_class

instance_num=0
instance_obj_list=[]
is_visible=True

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
                ("RANDOM", "Random", "Generate random pattern"),
                ("UNIFORM", "Uniform", "Generate uniform pattern")                
                ]
                
    type: bpy.props.EnumProperty(
    items=options_type,
    name="Type",
    description="Select the scatter distribution type",
    default="RANDOM"
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
        
        global instance_num
        global is_visible
        is_visible=True
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
        

class backdrop_gen(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.backdrop_gen"
    bl_label = "Generate Backdrop"
    bl_options = {"REGISTER", "UNDO"}
    bl_description="Creates the backdrop using given input"
    
    #@classmethod
    def scatter_obj(self):
        context=bpy.context
        global instance_num
        
        props=bpy.context.scene.bdg_props
        bg_color = props.bg_color
        instance_obj = props.instance_obj
        plat_color = props.plat_color
        #b_color = props.b_color
        #b_rad = props.b_rad
        num=props.num
        rot_randomness=props.rot_randomness
        seed=props.seed_num
        is_anim=props.is_anim
        #is_ball=props.is_ball
        is_plat=props.is_plat
        is_obj=props.is_obj
        type=props.type
        is_front=props.is_front
        loc_uni=props.loc_uni
        count=props.count
        offset=props.offset
        plat_rad=props.plat_rad
        spread_x=props.spread_x
        spread_z=props.spread_z
        obj_rot_speed=props.obj_rot_speed
        p_rot_speed=props.p_rot_speed
        #b_speed=props.b_speed
        obj_speed=props.obj_speed
        scale=props.scale_randomness
        l_intensity=props.l_intensity
        
        
        frame_start=bpy.context.scene.frame_start
        frame_end=bpy.context.scene.frame_end
        fps=bpy.context.scene.render.fps
        if instance_obj== None:
            is_obj=False
        else:
            instance_obj_list.append(instance_obj)
        
        
        if is_obj:
            if type=="UNIFORM":
                so = bpy.data.objects.new("bdg_instance_"+str(instance_num)+"_uniform", instance_obj_list[-1].data.copy())
                so.location=(loc_uni[0],loc_uni[1],loc_uni[2])
                so.data = instance_obj_list[-1].data
                so.modifiers.new(name="Array", type='ARRAY')
                so.modifiers.new(name="Array.001", type='ARRAY')
                so.modifiers["Array"].relative_offset_displace[0] = offset[0]
                so.modifiers["Array.001"].relative_offset_displace[0] = 0
                so.modifiers["Array.001"].relative_offset_displace[2] = offset[1]
                so.modifiers["Array"].count = count[0]
                so.modifiers["Array.001"].count = count[1]
                                
            else:    
                for i in range(num):
                    frame_num=0
                    bpy.context.scene.frame_set(frame_num)
                    r_scale=round(random.uniform(1-scale,1),4)
                    x_rot=round(random.uniform(-180*rot_randomness,180*rot_randomness),4)
                    y_rot=round(random.uniform(-180*rot_randomness,180*rot_randomness),4)
                    z_rot=round(random.uniform(-180*rot_randomness,180*rot_randomness),4)
                    x=round(random.uniform(-1.5*spread_x,1.5*spread_x),4)
                    if is_front:
                        y=round(random.uniform(-4,4),4)
                    else:
                        y=round(random.uniform(plat_rad+0.5,4),4)
                    z=round(random.uniform(0.3,2*spread_z),4)
                    so = bpy.data.objects.new("bdg_instance_"+str(instance_num), instance_obj_list[-1].data.copy())
                    so.data = instance_obj_list[-1].data
                    
                    so.location=(x,y,z)
                    so.rotation_euler=(math.radians(x_rot),math.radians(y_rot),math.radians(z_rot))
                    so.scale=(r_scale,r_scale,r_scale)
                    
                    if is_anim:
                        loc_data=[]
                        rot_data=[]
                        #so.keyframe_insert(data_path="location",index=-1)
                        #so.keyframe_insert(data_path="rotation_euler",index=-1)
                        bpy.context.scene.frame_set(frame_num)
                        so.keyframe_insert(data_path="location",index=0)
                        so.keyframe_insert(data_path="rotation_euler",index=0)
                        frame_num+=fps
                        bpy.context.scene.frame_set(frame_num)
                        so.keyframe_insert(data_path="location",index=1)
                        so.keyframe_insert(data_path="rotation_euler",index=1)
                        frame_num+=fps
                        bpy.context.scene.frame_set(frame_num)
                        so.keyframe_insert(data_path="location",index=2)
                        so.keyframe_insert(data_path="rotation_euler",index=2)
                        frame_num+=fps*3
                        loc_data.append((x,y,z))
                        rot_data.append((math.radians(x_rot),math.radians(y_rot),math.radians(z_rot)))
                        
                        #for j in range(4):
                        while (frame_num<frame_end):
                            bpy.context.scene.frame_set(frame_num)
                            x_dev=round(obj_speed*random.uniform(-0.4,0.4),4)
                            y_dev=round(obj_speed*random.uniform(-0.4,0.4),4)
                            z_dev=round(obj_speed*random.uniform(-0.4,0.4),4)
                            so.location=(x+x_dev,y+y_dev,z+y_dev)
                            #so.location=(x+obj_speed*random.uniform(-0.2,0.2),y+obj_speed*random.uniform(-0.2,0.2),z+obj_speed*random.uniform(0,0.2))
                            scale_dev=round(random.uniform(-0.1,0.1),4)
                            rot_dev=round(random.uniform(-180*obj_rot_speed,180*obj_rot_speed),4)
                            while (rot_dev<30 and rot_dev>-30 and 180*obj_rot_speed>30):
                                rot_dev=round(random.uniform(-90*obj_rot_speed,90*obj_rot_speed),4)
                            so.scale=(r_scale+scale_dev,r_scale+scale_dev,r_scale+scale_dev)
                            so.rotation_euler=(math.radians(x_rot+rot_dev),math.radians(y_rot+rot_dev),math.radians(z_rot+rot_dev))
                            loc_data.append((x+x_dev,y+y_dev,z+y_dev))
                            rot_data.append((math.radians(x_rot+rot_dev),math.radians(y_rot+rot_dev),math.radians(z_rot+rot_dev)))
                            #frame_num+=((frame_end-frame_start)//3)+1
                            #so.keyframe_insert(data_path="location",index=-1)
                            #so.keyframe_insert(data_path="scale",index=-1)
                            #so.keyframe_insert(data_path="rotation_euler",index=-1)
                            so.keyframe_insert(data_path="location",index=0)
                            so.keyframe_insert(data_path="rotation_euler",index=0)
                            frame_num-=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=1)
                            so.keyframe_insert(data_path="rotation_euler",index=1)
                            frame_num+=fps*2
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=2)
                            so.keyframe_insert(data_path="rotation_euler",index=2)
                            frame_num+=fps*4
                            seed+=100
                            random.seed(seed)
                        else:
                            exp_frame=frame_num-5*fps
                            frame_num=frame_end
                            so.location=loc_data[0]
                            so.rotation_euler=rot_data[0]
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=0)
                            so.keyframe_insert(data_path="rotation_euler",index=0)
                            frame_num+=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=1)
                            so.keyframe_insert(data_path="rotation_euler",index=1)
                            frame_num+=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=2)
                            so.keyframe_insert(data_path="rotation_euler",index=2)
                            frame_num=frame_start-frame_end+exp_frame
                            so.location=loc_data[1]
                            so.rotation_euler=rot_data[1]
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=0)
                            so.keyframe_insert(data_path="rotation_euler",index=0)
                            frame_num-=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=1)
                            so.keyframe_insert(data_path="rotation_euler",index=1)
                            frame_num+=2*fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=2)
                            so.keyframe_insert(data_path="rotation_euler",index=2)
                            seed+=100
                            random.seed(seed)
                            
            bpy.context.scene.frame_set(0)
                
    def execute(self, context):
        
        global instance_num
        global is_visible
        is_visible=True
        instance_num=1
        props=bpy.context.scene.bdg_props
        bg_color = props.bg_color
        instance_obj = props.instance_obj
        plat_color = props.plat_color
        #b_color = props.b_color
        #b_rad = props.b_rad
        num=props.num
        rot_randomness=props.rot_randomness
        seed=props.seed_num
        is_anim=props.is_anim
        #is_ball=props.is_ball
        is_plat=props.is_plat
        is_obj=props.is_obj
        type=props.type
        is_front=props.is_front
        loc_uni=props.loc_uni
        count=props.count
        offset=props.offset
        plat_rad=props.plat_rad
        spread_x=props.spread_x
        spread_z=props.spread_z
        obj_rot_speed=props.obj_rot_speed
        p_rot_speed=props.p_rot_speed
        #b_speed=props.b_speed
        obj_speed=props.obj_speed
        scale=props.scale_randomness
        l_intensity=props.l_intensity
        
        
        frame_start=bpy.context.scene.frame_start
        frame_end=bpy.context.scene.frame_end
        fps=bpy.context.scene.render.fps
        if instance_obj== None:
            is_obj=False
        else:
            instance_obj_list.append(instance_obj)
        
        collection = bpy.data.collections.new("bdg_collection")
        bpy.context.scene.collection.children.link(collection)
        


        #materials
        
        if is_plat:
        #platform Cylinder material
            c_mat = bpy.data.materials.new(name="bdg_Platform Material")
            c_mat.use_nodes=True
            nodes=c_mat.node_tree.nodes
            m_out=nodes.get("Material Output")
            p_bsdf=nodes.get("Principled BSDF")
            p_bsdf.inputs[0].default_value=plat_color

        #BG material
        bg_mat = bpy.data.materials.new(name="bdg_BG Material")
        bg_mat.use_nodes=True
        nodes=bg_mat.node_tree.nodes
        m_out=nodes.get("Material Output")
        p_bsdf=nodes.get("Principled BSDF")
        p_bsdf.inputs[0].default_value=bg_color

        #camera 
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, -4.62028, 0.590903), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "bdg_camera"
        bpy.context.scene.camera = bpy.data.objects.get("bdg_camera")
        bpy.ops.object.select_all(action='DESELECT')

        #BG creation
        
        bpy.ops.mesh.primitive_plane_add(size=150,location=(0, 0, 0))
        obj = bpy.context.active_object
        if obj is not None:
            obj.name = "bdg_bg_plane"
            obj.data.materials.append(bg_mat)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.data.edges[3].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.extrude_edges_move()
            bpy.ops.transform.translate(value=(0, 0, 50))
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 20
            bpy.context.object.modifiers["Bevel"].segments = 10
            bpy.ops.object.shade_smooth()
        

        #platform creation
        if is_plat:
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=plat_rad, depth=0.1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            bpy.context.object.name = "bdg_platform"
            so = bpy.context.active_object
            so.data.materials.append(c_mat)
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.01
            bpy.context.object.modifiers["Bevel"].segments = 2
            bpy.ops.object.subdivision_set(level =3, relative=False)
            bpy.ops.object.shade_smooth()
                        
        #object scatter
        self.scatter_obj()
                        
            
        #Light Creation
        plight=bpy.ops.object.light_add(type='SPOT', radius=3, align='WORLD', location=(3, -1, 2), rotation=(0.902665, 0.409066, 1.0472), scale=(1, 1, 1))
        bpy.context.object.name = "bdg_light_point"
        bpy.context.object.data.energy=l_intensity*1500
        bpy.context.object.data.spot_size = 1.06465
        bpy.context.object.data.spot_blend = 0.329487
        bpy.context.object.data.shadow_soft_size = 1
        
        bglight=bpy.ops.object.light_add(type='AREA', radius=10, align='WORLD', location=(0, 1, 10), rotation=(1.48353, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "bdg_light_bg_1"
        bpy.context.object.data.energy = l_intensity*6000
        
        bglight2=bpy.ops.object.light_add(type='SPOT', align='WORLD', location=(0, 14, 10), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "bdg_light_bg_2"
        bpy.context.object.data.energy=l_intensity*75000
        bpy.context.object.data.shadow_soft_size = 20
        bpy.context.object.data.spot_size = 3.14
        bpy.context.object.data.spot_blend = 0.85696

        bglight3=bpy.ops.object.light_add(type='SPOT', radius=100, align='WORLD', location=(0, 40, 10), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "bdg_light_bg_3"
        bpy.context.object.data.energy = l_intensity*200000
        bpy.context.object.data.spot_size = 2.25671

        alight=bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-4, -1, 3), rotation=(1.39626, 0, -1.309), scale=(1, 1, 1))
        bpy.context.object.name = "bdg_light_a"
        bpy.context.object.data.energy=l_intensity*150
        
        #Empty Creation
        if is_anim:
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            bpy.context.object.name = "bdg_empty"
            so = bpy.context.active_object
            rot=0
            frame_num=0
            frame_start=bpy.context.scene.frame_start
            frame_end=bpy.context.scene.frame_end
            if is_anim:
                for i in range(5):
                    bpy.context.scene.frame_set(frame_num)
                    so.rotation_euler=(0,0,rot)
                    so.keyframe_insert(data_path="rotation_euler",index=-1)
                    rot+=p_rot_speed*3.14/3
                    frame_num+=(frame_end-frame_start)//3
        
        bpy.context.scene.frame_set(0)
        
        all_objects = bpy.data.objects

        bdg_objects = []

        for obj in all_objects:
            if obj.name.startswith("bdg_"):
                bdg_objects.append(obj)

        for obj in bdg_objects:
            if obj.name in bpy.context.collection.objects:
                bpy.context.collection.objects.unlink(obj)
            if obj.name not in collection.objects:
                collection.objects.link(obj)
        bpy.context.scene.frame_set(0)

            


        return {'FINISHED'}
    
    
    
class obj_scatter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.obj_scatter"
    bl_label = "Scatter Objects"
    bl_options = {"REGISTER", "UNDO"}
    bl_description="Scatters the selected object across the 3D space"
    
    #@classmethod
        
    def execute(self, context):
        global instance_num
        global is_visible
        is_visible=True
        props=bpy.context.scene.bdg_props
        bg_color = props.bg_color
        instance_obj = props.instance_obj
        plat_color = props.plat_color
        #b_color = props.b_color
        #b_rad = props.b_rad
        num=props.num
        rot_randomness=props.rot_randomness
        seed_num=props.seed_num
        is_anim=props.is_anim
        #is_ball=props.is_ball
        is_plat=props.is_plat
        is_obj=props.is_obj
        type=props.type
        is_front=props.is_front
        loc_uni=props.loc_uni
        count=props.count
        offset=props.offset
        plat_rad=props.plat_rad
        spread_x=props.spread_x
        spread_z=props.spread_z
        obj_rot_speed=props.obj_rot_speed
        p_rot_speed=props.p_rot_speed
        #b_speed=props.b_speed
        obj_speed=props.obj_speed
        scale=props.scale_randomness
        l_intensity=props.l_intensity
        
        
        frame_start=bpy.context.scene.frame_start
        frame_end=bpy.context.scene.frame_end
        fps=bpy.context.scene.render.fps
        
        if instance_obj== None:
            is_obj=False
        else:
            instance_obj_list.append(instance_obj)
        instance_num+=1
                
        if is_obj:
            if type=="UNIFORM":
                
                so = bpy.data.objects.new("bdg_instance_"+str(instance_num)+"_uniform", instance_obj_list[-1].data.copy())
                collection = bpy.data.collections.get("bdg_collection")
                if collection == None :
                    collection = bpy.data.collections.new("bdg_collection")
                    bpy.context.scene.collection.children.link(collection)
                    collection = bpy.data.collections.get("bdg_collection")
                collection.objects.link(so)
                so.location=(loc_uni[0],loc_uni[1],loc_uni[2])
                so.data = instance_obj_list[-1].data
                so.modifiers.new(name="Array", type='ARRAY')
                so.modifiers.new(name="Array.001", type='ARRAY')
                so.modifiers["Array"].relative_offset_displace[0] = offset[0]
                so.modifiers["Array.001"].relative_offset_displace[0] = 0
                so.modifiers["Array.001"].relative_offset_displace[2] = offset[1]
                so.modifiers["Array"].count = count[0]
                so.modifiers["Array.001"].count = count[1]
            else: 
                for i in range(num):
                    frame_num=0
                    bpy.context.scene.frame_set(frame_num)
                    r_scale=random.uniform(1-scale,1)
                    x_rot=random.uniform(0,360*rot_randomness)
                    y_rot=random.uniform(0,360*rot_randomness)
                    z_rot=random.uniform(0,360*rot_randomness)
                    x=random.uniform(-1.5*spread_x,1.5*spread_x)
                    if is_front:
                        y=random.uniform(-4,4)
                    else:
                        y=random.uniform(plat_rad+0.5,4)
                    z=random.uniform(0.3,2*spread_z)
                    so = bpy.data.objects.new("bdg_instance_"+str(instance_num), instance_obj_list[-1].data.copy())
                    so.data = instance_obj_list[-1].data
                    collection = bpy.data.collections.get("bdg_collection")
                    if collection == None :
                        collection = bpy.data.collections.new("bdg_collection")
                        bpy.context.scene.collection.children.link(collection)
                        collection = bpy.data.collections.get("bdg_collection")
                    collection.objects.link(so)
                    so.location=(x,y,z)
                    so.rotation_euler=(x_rot,y_rot,z_rot)
                    so.scale=(r_scale,r_scale,r_scale)
                    if is_anim:
                        loc_data=[]
                        rot_data=[]
                        so.keyframe_insert(data_path="location",index=0)
                        so.keyframe_insert(data_path="rotation_euler",index=0)
                        frame_num+=fps
                        bpy.context.scene.frame_set(frame_num)
                        so.keyframe_insert(data_path="location",index=1)
                        so.keyframe_insert(data_path="rotation_euler",index=1)
                        frame_num+=fps
                        bpy.context.scene.frame_set(frame_num)
                        so.keyframe_insert(data_path="location",index=2)
                        so.keyframe_insert(data_path="rotation_euler",index=2)
                        frame_num+=fps*3
                        loc_data.append((x,y,z))
                        rot_data.append((math.radians(x_rot),math.radians(y_rot),math.radians(z_rot)))
                        
                        #for j in range(4):
                        while (frame_num<frame_end):
                            bpy.context.scene.frame_set(frame_num)
                            x_dev=obj_speed*random.uniform(-0.2,0.2)
                            y_dev=obj_speed*random.uniform(-0.2,0.2)
                            z_dev=obj_speed*random.uniform(-0.2,0.2)
                            so.location=(x+x_dev,y+y_dev,z+y_dev)
                            scale_dev=random.uniform(-0.1,0.1)
                            rot_dev=random.uniform(0,180*obj_rot_speed)
                            while (rot_dev<30):
                                rot_dev=random.uniform(-90*obj_rot_speed,90*obj_rot_speed)
                            so.scale=(r_scale+scale_dev,r_scale+scale_dev,r_scale+scale_dev)
                            so.rotation_euler=(math.radians(x_rot+rot_dev),math.radians(y_rot+rot_dev),math.radians(z_rot+rot_dev))
                            loc_data.append((x+x_dev,y+y_dev,z+y_dev))
                            rot_data.append((math.radians(x_rot+rot_dev),math.radians(y_rot+rot_dev),math.radians(z_rot+rot_dev)))
                            so.keyframe_insert(data_path="location",index=0)
                            so.keyframe_insert(data_path="rotation_euler",index=0)
                            frame_num-=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=1)
                            so.keyframe_insert(data_path="rotation_euler",index=1)
                            frame_num+=fps*2
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=2)
                            so.keyframe_insert(data_path="rotation_euler",index=2)
                            frame_num+=fps*4
                        else:
                            frame_num=frame_end
                            so.location=loc_data[0]
                            so.rotation_euler=rot_data[0]
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=0)
                            so.keyframe_insert(data_path="rotation_euler",index=0)
                            frame_num+=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=1)
                            so.keyframe_insert(data_path="rotation_euler",index=1)
                            frame_num+=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=2)
                            so.keyframe_insert(data_path="rotation_euler",index=2)
                            frame_num=frame_start-5*fps
                            so.location=loc_data[1]
                            so.rotation_euler=rot_data[1]
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=0)
                            so.keyframe_insert(data_path="rotation_euler",index=0)
                            frame_num-=fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=1)
                            so.keyframe_insert(data_path="rotation_euler",index=1)
                            frame_num+=2*fps
                            bpy.context.scene.frame_set(frame_num)
                            so.keyframe_insert(data_path="location",index=2)
                            so.keyframe_insert(data_path="rotation_euler",index=2)
                            print(loc_data)
                            
            bpy.context.scene.frame_set(0)
                    
        bpy.context.scene.frame_set(0)    
        return {'FINISHED'}
    

class del_scene(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.del_scene"
    bl_label = "Delete Scene" 
    bl_options = {"REGISTER", "UNDO"}  
    bl_description="Deletes the the whole BDG scene"     
    
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
    bl_description="Deletes the last instance of scattered objects"    
    
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

class hide_obj(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.hide_obj"
    bl_label = "Hide Objects" 
    bl_options = {"REGISTER", "UNDO"}    
    bl_description="Hides the scattered objects in viewport"    
    
    def execute(self,context):
        global is_visible
        is_visible=False
        for obj in bpy.data.objects:
            if obj.name.startswith("bdg_instance_"):
                obj.hide_viewport=True
        print("hide")
        return {'FINISHED'}

class unhide_obj(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.unhide_obj"
    bl_label = "Unhide Objects" 
    bl_options = {"REGISTER", "UNDO"} 
    bl_description="Unhides the scattered objects in viewport"         
    
    def execute(self,context):

        global is_visible
        is_visible=True
        for obj in bpy.data.objects:
            if obj.name.startswith("bdg_instance_"):
                obj.hide_viewport= False
        
        return {'FINISHED'}

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
        global is_visible
        row = layout.row()
        row.prop(props,"is_obj")
        #row.prop(props,"is_ball")
        row.prop(props,"is_plat")
        row = layout.row()
        if props.is_obj :
            row.prop(props,"instance_obj")
            row = layout.row()
            if props.instance_obj is not None:
                row.prop(props,"type")
            else:
                row.label(text= "Select an object to scatter",icon="ERROR")
            row = layout.row()
        if props.is_plat:
            row.prop(props,"plat_rad")
            row = layout.row()
        if props.is_obj and props.instance_obj is not None:    
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
                    if props.is_obj and props.instance_obj is not None:
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
        row.operator("object.backdrop_gen",icon="PROP_ON")
        if props.is_obj:
            row = layout.row()
            if props.instance_obj is not None:
                row.operator("object.obj_scatter",icon="PROP_CON")
            row.operator("object.del_obj",icon="CANCEL")
        row = layout.row()
        if is_visible:
            row.operator("object.hide_obj",icon="HIDE_OFF")
        else:
            row.operator("object.unhide_obj",icon="HIDE_ON")
        row = layout.row()
        row.operator("object.del_scene",icon="TRASH")
        


# Registration

_classes = [
    backdrop_gen,
    bdg_panel,
    obj_scatter,
    del_scene,
    hide_obj,
    unhide_obj,
    del_obj
    
]

def register():
    for c in _classes:
        register_class(c)

def unregister():
    for c in _classes:
        unregister_class(c)
    


if __name__ == "__main__":
    register()
