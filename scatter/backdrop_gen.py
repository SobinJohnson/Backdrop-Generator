import bpy
import math
import random
from bpy.utils import register_class, unregister_class

from ..global_var import *
from ..panel.bdg_panel import bdg_props

bpy.types.Scene.bdg_props = bpy.props.PointerProperty(type=bdg_props)

class scene_gen(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.backdrop_gen"
    bl_label = "Generate Backdrop"
    bl_options = {"REGISTER", "UNDO"}
    
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
    
    #@classmethod
        
    def execute(self, context):
        global instance_num
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
    
    
_classes = [
    scene_gen,
    obj_scatter   
]

def register():
    for c in _classes:
        register_class(c)

def unregister():
    for c in _classes:
        unregister_class(c) 
