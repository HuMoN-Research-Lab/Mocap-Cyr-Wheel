import numpy as np, bpy, csv
from mathutils import Matrix, Vector, Euler
from math import *
import time

#Start frame of data
frame_start = 19655

#Start frame of data
frame_end = frame_start + 1

#default number of frames to output is all of them - change this value to an integer if you 
#want to output less 
#set to "all" to output all frames
num_frames_output = "all"
#Change: the path of the tsv file 
input_tsv = r"/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/WheelForcePlate0007.tsv"
#input force plate data
input_force_plate = r"/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/Force_Plate_Data/WheelForcePlate0007_f_1.tsv"
#Change: the path of the folder you want to export xml file and png frames of animation to
output_frames_folder = "/Users/jackieallex/Downloads/Mocap-Cyr-Wheel"


#script to read tsv files in blender

#read force plate data 
#open file (adjust file location)
def create_data_arr_force_plate(frame):
    current_row = force_file[frame + 27]
    cols, rows = (3, 3)
    arr = [[None]*cols for _ in range(rows)]
    count = 0
    count_row = 0
    for x in range(2, 11):
        if count == 3:
            count = 0
            count_row += 1
        arr[count_row][count] = current_row[x]
        count += 1
    return arr
    

with open(input_force_plate, "r") as tsv_file:
    force_file = list(csv.reader(tsv_file, delimiter='\t'))
    #the data from the starting frame
    frame = frame_start
    force_plate_arr =  create_data_arr_force_plate(frame)


for obj in bpy.context.scene.objects:
    if obj.name.startswith("Arrow-bottom"):
        arrow_bottom = obj
    if obj.name.startswith("Arrow-top"):
        arrow_top = obj
    if obj.name.startswith("Cone"):
        cone = obj

# Create 2D array "arr" to hold all 3D coordinate info of markers
#numerical data begins in column 11
def create_data_arr(frame):
    current_row = file[frame + 11]
    cols, rows = (3, int((len(current_row) - 2) / 3))
    arr = [[None]*cols for _ in range(rows)]
    count = 0
    count_row = 0
    for x in range(2, len(current_row)):
        arr[count_row][count] = current_row[x]
        count += 1
        if (count == 3):
            count = 0
            count_row += 1
    return arr;
 
#-----------------------------------------------------------------------------------
#open file (adjust file location)
with open(input_tsv, "r") as tsv_file:
    file = list(csv.reader(tsv_file, delimiter='\t'))
    #the data from the starting frame
    frame = frame_start
    arr = create_data_arr(frame)
            
#-----------------------------------------------------------------------------------
#Create an array of marker names 
#column 9 of tsv file holds all marker names
current_row = file[9] 
name_arr = []
for index in range(1, len(current_row)):
    name_arr.append(current_row[index])
        
#-----------------------------------------------------------------------------------
#Create empties at marker positions    
name = 0
order_of_markers = []
# make sure project unity is correct for imported data
bpy.context.scene.unit_settings.length_unit = 'METERS'
#iterate through arr and create an empty object at that location for each element
for col in arr:
    # parse string float value into floats, create Vector, set empty position to Vector
    # multiply by .001 because original data is recorded in millimeters, but we want meters for this project
    coord = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, float(col[2]) * 0.001))
    bpy.ops.object.add(type='EMPTY', location=coord)  
    mt = bpy.context.active_object  
    #get name from name array "name_arr"
    mt.name = name_arr[name]
    #increment name of empty
    name += 1
    #link empty to this scene
    bpy.context.scene.collection.objects.link( mt )
    #set empty location
    mt.location = coord
    #set empty display size
    mt.empty_display_size = 0.1
    #add empty to array order_of_markers so we can later access it 
    order_of_markers.append(mt)
    
#Create armature object
armature = bpy.data.armatures.new('Armature')
armature_object = bpy.data.objects.new('Armature', armature)
#Link armature object to our scene
bpy.context.collection.objects.link(armature_object)
#Make armature variable
armature_data = bpy.data.objects[armature_object.name]
#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)

#create a mesh of armature
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
mesh = bpy.data.meshes.new("outline_skeleton_mesh")  # add the new mesh
obj = bpy.data.objects.new("outline_skeleton_object", mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

#list of all markers in order of array order_of_markers
arr_markers_sanity_check = ['MARKER_NAMES', '0Steve_HeadL', '1Steve_HeadTop', '2Steve_HeadR', 
    '3Steve_HeadFront', '4Steve_LShoulderTop', '5Steve_LShoulderBack', 
    '6Steve_LArm', '7Steve_LElbowOut', '8Steve_LWristOut', '9Steve_LWristIn', 
    '10Steve_LHandOut', '11Steve_RShoulderTop', '12Steve_RShoulderBack', 
    '13Steve_RArm', '14Steve_RElbowOut', '15Steve_RWristOut', '16Steve_RWristIn', 
    '17Steve_RHandOut', '18Steve_Chest', '19Steve_SpineTop', '20Steve_BackL', 
    '21Steve_BackR', '22Steve_WaistLFront', '23Steve_WaistLBack', 
    '24Steve_WaistRBack', '25Steve_WaistRFront', '26Steve_LThigh', 
    '27Steve_LKneeOut', '28Steve_LShin', '29Steve_LAnkleOut', 
    '30Steve_LHeelBack', '31Steve_LForefootOut', '32Steve_LToeTip', 
    '33Steve_LForefootIn', '34Steve_RThigh', '35Steve_RKneeOut', '36Steve_RShin', 
    '37Steve_RAnkleOut', '38Steve_RHeelBack', '39Steve_RForefootOut', 
    '40Steve_RToeTip', '41Steve_RForefootIn', '42Steve_CyrWheel01', 
    '43Steve_CyrWheel02', '44Steve_CyrWheel03', '45Steve_CyrWheel04', 
    '46Steve_CyrWheel05']

#--------------------------------------------------------------------------
#Create mesh outline of skeleton parts
 # verts made with XYZ coords
verts = []
faces = []
iter = 0;
for x in order_of_markers:
    #add each marker location from order_of_markers to create a vertice there
    verts.append(x.location)

#edges mesh connect
#connect: [(1Steve_HeadTop,2Steve_HeadR),(2Steve_HeadR,3Steve_HeadFront),(3Steve_HeadFront,0Steve_HeadL), 
# (0Steve_HeadL,1Steve_HeadTop),(1Steve_HeadTop,3Steve_HeadFront),

# (19Steve_SpineTop,18Steve_Chest),(18Steve_Chest,21Steve_BackR),(18Steve_Chest,20Steve_BackL), (20Steve_BackL,21Steve_BackR),
# (21Steve_BackR,19Steve_SpineTop),(20Steve_BackL,19Steve_SpineTop), 

# (11Steve_RShoulderTop,12Steve_RShoulderBack),(11Steve_RShoulderTop,14Steve_RElbowOut),(12Steve_RShoulderBack,13Steve_RArm), 
# (14Steve_RElbowOut,13Steve_RArm),(14Steve_RElbowOut,15Steve_RWristOut),(15Steve_RWristOut,16Steve_RWristIn), 
# (15Steve_RWristOut,17Steve_RHandOut)


#(4Steve_LShoulderTop,5Steve_LShoulderBack), (4Steve_LShoulderTop,7Steve_LElbowOut), (5Steve_LShoulderBack,6Steve_LArm),
#(7Steve_LElbowOut,6Steve_LArm),(7Steve_LElbowOut,8Steve_LWristOut), (8Steve_LWristOut,9Steve_LWristIn),
#(8Steve_LWristOut,10Steve_LHandOut),

#(22Steve_WaistLFront,25Steve_WaistRFront),(22Steve_WaistLFront,23Steve_WaistLBack),
# (25Steve_WaistRFront,24Steve_WaistRBack), (23Steve_WaistLBack,24Steve_WaistRBack),

#(25Steve_WaistRFront,34Steve_RThigh),(24Steve_WaistRBack,35Steve_RKneeOut),(34Steve_RThigh,35Steve_RKneeOut),
# (35Steve_RKneeOut,36Steve_RShin),(35Steve_RKneeOut,37Steve_RAnkleOut),(37Steve_RAnkleOut,38Steve_RHeelBack),
# (38Steve_RHeelBack,39Steve_RForefootOut),(38Steve_RHeelBack,41Steve_RForefootIn),(41Steve_RForefootIn,40Steve_RToeTip), 
# (36Steve_RShin,37Steve_RAnkleOut), (39Steve_RForefootOut,40Steve_RToeTip), 

# (22Steve_WaistLFront,26Steve_LThigh),(23Steve_WaistLBack,27Steve_LKneeOut),(26Steve_LThigh,27Steve_LKneeOut),
# (27Steve_LKneeOut,28Steve_LShin),(27Steve_LKneeOut,29Steve_LAnkleOut),(29Steve_LAnkleOut,30Steve_LHeelBack),
#  (30Steve_LHeelBack,31Steve_LForefootOut), (30Steve_LHeelBack,33Steve_LForefootIn),(33Steve_LForefootIn,32Steve_LToeTip),
# (28Steve_LShin,29Steve_LAnkleOut), (31Steve_LForefootOut,32Steve_LToeTip)]


edges =  [(1,2),(2,3),(3,0),(0,1),(1,3), #head
#chest and back
(19,18),(18,21),(18,20),(20,21),(21,19),(20,19),
#Right shoulder and arm
(11,12),(11,14),(12,13),(14,13),(14,15),(15,16), (15,17),
#Left shoulder and arm
(4,5),(4,7),(5,6),(7,6),(7,8),(8,9), (8,10),
#Waist
(22,25),(22,23),(25,24),(23,24),
#Right Leg and foot
(25,34),(24,35),(34,35),(35,36),(35,37),(37,38), (38,39),
(38,41),(41,40),(36,37), (39,40),
#left leg and foot
(22,26),(23,27),(26,27),(27,28),(27,29),(29,30), (30,31),
(30,33),(33,32),(28,29), (31,32)]

#Create the mesh with the vertices and faces
obj.data.from_pydata(verts, edges, faces)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
#Set origin of the plane to its median center
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

#Add screw modifier to make it thicker and visible in render
bpy.ops.object.modifier_add(type='SCREW')
bpy.context.object.modifiers["Screw"].angle = 0
bpy.context.object.modifiers["Screw"].steps = 2
bpy.context.object.modifiers["Screw"].render_steps = 2
bpy.context.object.modifiers["Screw"].screw_offset = 0.01
bpy.context.object.modifiers["Screw"].use_merge_vertices = True

#Add vertex groups to have each part of mesh controlled by hooks and corresponding empty object
def add_vertex_group_hooks():
    for x in range(len(verts)):
        #Create vertex groups, one for each vertex
        vg = obj.vertex_groups.new(name="group" + str(x))
        vg.add([x], 1, "ADD")
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='HOOK')
        hook_name = "Hook" + str(x)
        bpy.context.object.modifiers["Hook"].name = hook_name
        bpy.context.object.modifiers[hook_name].object = order_of_markers[x]
        bpy.context.object.modifiers[hook_name].vertex_group = "group" + str(x)
        
add_vertex_group_hooks()

outline_mesh_obob = obj


#force plate mesh
'''
FORCE_PLATE_CORNER_POSX_POSY_X	353.011101
FORCE_PLATE_CORNER_POSX_POSY_Y	1295.030594
FORCE_PLATE_CORNER_POSX_POSY_Z	-2.6015
FORCE_PLATE_CORNER_NEGX_POSY_X	747.085989
FORCE_PLATE_CORNER_NEGX_POSY_Y	1294.596434
FORCE_PLATE_CORNER_NEGX_POSY_Z	-2.6923
FORCE_PLATE_CORNER_NEGX_NEGY_X	746.431708
FORCE_PLATE_CORNER_NEGX_NEGY_Y	700.785577
FORCE_PLATE_CORNER_NEGX_NEGY_Z	-2.1361
FORCE_PLATE_CORNER_POSX_NEGY_X	352.357
FORCE_PLATE_CORNER_POSX_NEGY_Y	701.219738
FORCE_PLATE_CORNER_POSX_NEGY_Z	-2.0453
'''
X_corner_pos = Vector((353.011101* 0.001, 1295.030594* 0.001, -2.6015* 0.001))
X_corner_neg = Vector((747.085989* 0.001, 1294.596434* 0.001, -2.6923* 0.001))
Neg_x_neg = Vector((746.431708* 0.001, 700.785577* 0.001, -2.1361* 0.001))
pos_x_neg = Vector((352.357* 0.001, 701.219738* 0.001, -2.0453* 0.001))


mesh_f = bpy.data.meshes.new("force_plate")  # add the new mesh
obj_f = bpy.data.objects.new("force_plate_object", mesh_f)
col = bpy.data.collections.get("Collection")
col.objects.link(obj_f)
bpy.context.view_layer.objects.active = obj_f

verts_f = [X_corner_pos, X_corner_neg, Neg_x_neg, pos_x_neg]
edges_f =  [(0,1),(1,2),(2,3),(3,0)]

#Create the mesh with the vertices and faces
obj_f.data.from_pydata(verts_f, edges_f, [])
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj_f
obj_f.select_set(state=True)
#Set origin of the plane to its median center
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

a = [353.011101* 0.001, 1295.030594* 0.001, -2.6015* 0.001]
b = [747.085989* 0.001, 1294.596434* 0.001, -2.6923* 0.001]
c = [746.431708* 0.001, 700.785577* 0.001, -2.1361* 0.001]
d = [352.357* 0.001, 701.219738* 0.001, -2.0453* 0.001]

plate_origin =  [(a1 + b1 + c1 + d1) / 4 for a1, b1, c1, d1  in zip(a, b, c, d)]

arrow_bottom.location = plate_origin

bpy.context.view_layer.objects.active = obj_f
obj_f.select_set(state=True)
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0.00118261, -0.0109036, 0.00548362), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
#bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0.00142037, 1.1027e-05, 0.0276659), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.mesh.edge_face_add()




#create arrow mesh

#create a mesh of armature
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
mesh_arrow = bpy.data.meshes.new("mesh_arrow")  # add the new mesh
obj_arrow = bpy.data.objects.new("obj_arrow", mesh_arrow)
col = bpy.data.collections.get("Collection")
col.objects.link(obj_arrow)
bpy.context.view_layer.objects.active = obj_arrow

verts_arrow = [arrow_bottom.location, arrow_top.location]
faces_arrow = []
edges_arrow =  [(0,1)]


#Create the mesh with the vertices and faces
obj_arrow.data.from_pydata(verts_arrow, edges_arrow, faces_arrow)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj_arrow
obj_arrow.select_set(state=True)
#Set origin of the plane to its median center
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

#Add screw modifier to make it thicker and visible in render
bpy.ops.object.modifier_add(type='SCREW')
bpy.context.object.modifiers["Screw"].angle = 0
bpy.context.object.modifiers["Screw"].steps = 2
bpy.context.object.modifiers["Screw"].render_steps = 2
bpy.context.object.modifiers["Screw"].screw_offset = 0.11
bpy.context.object.modifiers["Screw"].use_merge_vertices = True

order_of_arrow = [arrow_bottom, arrow_top]

for x in range(len(verts_arrow)):
    bpy.context.view_layer.objects.active = obj_arrow
    obj_arrow.select_set(state=True)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #Create vertex groups, one for each vertex
    vg = obj_arrow.vertex_groups.new(name="group" + str(x))
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    vg.add([x], 1, "ADD")
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj_arrow
    bpy.ops.object.modifier_add(type='HOOK')
    hook_name = "Hook" + str(x)
    bpy.context.object.modifiers["Hook"].name = hook_name
    bpy.context.object.modifiers[hook_name].object = order_of_arrow[x]
    bpy.context.object.modifiers[hook_name].vertex_group = "group" + str(x)

#--------------------------------------------------------------
#Virtual Markers!

#Three types of marker relationships:

# - "weight": the weighted average of multiple markers. the virtual_markers[x] contains the 
#list of markers that affect this virtual one. the weights[x] contains their corresponding weights in order.

# - "xyz": given 3 markers recorded in virtual_markers[x] (can repeat the same marker as two of the three), make this virtual marker
# have the x_pos of the first, the y_pos of the second, and the z_pos of the third

# - "offset": this virtual marker will have the position of another marker, but can be offset by an amount on the 
#x, y, and/or z axis. The marker will be recorded in virtual_markers[x][0] and the amount offset on each axis 
#will be recorded in weights[]


#Create marker methods for each different type of relationship:
#Create virtual markers takes in a string name and a list of marker s that influence it and weights
def create_marker_weight(name, markers, weighted):
    center = Vector((0, 0, 0))
    weight_iter = 0
    for x in markers:
        center += x.location*weighted[weight_iter]
        weight_iter += 1
    coord = Vector((float(center[0]), float(center[1]), float(center[2])))
    bpy.ops.object.add(type='EMPTY', location=coord)
    mt = bpy.context.active_object  
    mt.name = name
    bpy.context.scene.collection.objects.link( mt )
    mt.location = coord
    mt.empty_display_size = 0.2
    virtual_markers.append(mt)
    
#Create virtual markers takes in a string name 
#surrounding_markers [a, b, c] take a.x, b.y, and c.z locations
#z is up, x is forward, y is side
def create_marker_xyz(name, list):
    coord = Vector((list[0].location[0], list[1].location[1], list[2].location[2]))
    bpy.ops.object.add(type='EMPTY', location=coord)
    mt = bpy.context.active_object  
    mt.name = name
    bpy.context.scene.collection.objects.link( mt )
    mt.location = coord
    mt.empty_display_size = 0.2
    virtual_markers.append(mt)
    
#Create virtual markers takes in a string name and a list of marker s that influence it and weights
def create_marker_offset(name, markers, weighted):
    center = markers[0].location
    for index in range(len(weighted)):
        center[index] += weighted[index]
    coord = Vector((float(center[0]), float(center[1]), float(center[2])))
    bpy.ops.object.add(type='EMPTY', location=coord)
    mt = bpy.context.active_object  
    mt.name = name
    bpy.context.scene.collection.objects.link( mt )
    mt.location = coord
    mt.empty_display_size = 0.2
    virtual_markers.append(mt)


v_relationship = []
virtual_markers = []
surrounding_markers = []
weights = []
v_names = []

#updates data and creates virtual marker
def update_virtual_data(relationship, surrounding, vweights, vname):
    v_relationship.append(relationship)
    surrounding_markers.append(surrounding)
    weights.append(vweights)
    v_names.append(vname)
    if(relationship is "weight"):
        create_marker_weight(vname, surrounding, vweights)
    elif(relationship is "xyz"):
        create_marker_xyz(vname, surrounding)
    else:
        create_marker_offset(vname, surrounding, vweights)
        
    
#-----------------------------------------------------------------
#Define relationships and create virtual markers


#Wrists: Halfway between 15Steve_RWristOut and 16Steve_RWristIn/ 8Steve_LWristOut and 9Steve_LWristIn
l0 = [order_of_markers[15], order_of_markers[16]]
w0 = [0.5, 0.5]
update_virtual_data("weight", l0, w0, "v_R_Wrist")


l1 = [order_of_markers[8], order_of_markers[9]]
w1 = [0.5, 0.5]
update_virtual_data("weight", l1, w1, "v_L_Wrist")

#Hands: Halfway between 9Steve_LWristIn and 10Steve_LHandOut/16Steve_RWristIn and 17Steve_RHandOut
l2 = [order_of_markers[9], order_of_markers[10]]
w2 = [0.5, 0.5]
update_virtual_data("weight", l2, w2, "v_L_Hand")

l3 = [order_of_markers[16], order_of_markers[17]]
w3 = [0.5, 0.5]
update_virtual_data("weight", l3, w3, "v_R_Hand")

#elbows : X is v_L_Wrist (virtual_markers[1]), 
#Y is 7Steve_LElbowOut (order_of_markers[7]), 
#Z is 7Steve_LElbowOut (order_of_markers[7]) 
l4 = [order_of_markers[7]]
w4 = [.05, 0.0, 0.0]
update_virtual_data("offset", l4, w4, "v_L_Elbow")


#X is v_R_Wrist (virtual_markers[0], 
#Y is 14Steve_RElbowOut (order_of_markers[14]),
#and Z is 14Steve_RElbowOut (order_of_markers[14])
l5 = [order_of_markers[14]]
w5 = [.05, 0.0, 0.0]
update_virtual_data("offset", l5, w5, "v_R_Elbow") 

#Shoulders
#between 11Steve_RShoulderTop and 12Steve_RShoulderBack
l6 = [order_of_markers[11], order_of_markers[12]]
w6 = [0.75, 0.25]
update_virtual_data("weight", l6, w6, "v_R_Shoulder") 

#between 4Steve_LShoulderTop and 5Steve_LShoulderBack
l7 = [order_of_markers[4], order_of_markers[5]]
w7 = [0.75, 0.25]
update_virtual_data("weight", l7, w7, "v_L_Shoulder") 
    
#Chest between 19Steve_SpineTop, 18Steve_Chest, 21Steve_BackR, 20Steve_BackL
l8 = [order_of_markers[19], order_of_markers[18], order_of_markers[21], order_of_markers[20]]
w8 = [0.35, 0.35, 0.15, 0.15]
update_virtual_data("weight", l8, w8, "v_Chest") 

#Head between 1Steve_HeadTop, 0Steve_HeadL, 2Steve_HeadR, 3Steve_HeadFront
l9 = [order_of_markers[1], order_of_markers[0], order_of_markers[2], order_of_markers[3]]
w9 = [0.33333, 0.33333, 0.33333, 0]
update_virtual_data("weight", l9, w9, "v_Head") 

#Spine

#Spine1 between 3Steve_HeadFront and 19Steve_SpineTop
l10 = [order_of_markers[3], order_of_markers[19]]
w10 = [0.66666, 0.33333]
update_virtual_data("weight", l10, w10, "v_Spine1") 

#Spine2 between 19Steve_SpineTop and 18Steve_Chest
l11 = [order_of_markers[19], order_of_markers[18]]
w11 = [0.66666, 0.33333]
update_virtual_data("weight", l11, w11, "v_Spine2") 

#Spine3 between 19Steve_SpineTop, 18Steve_Chest, 21Steve_BackR, 20Steve_BackL
l12 = [order_of_markers[19], order_of_markers[18], order_of_markers[21], order_of_markers[20]]
w12 = [0.25, 0.25, 0.25, 0.25]
update_virtual_data("weight", l12, w12, "v_Spine3") 

#Spine4 between 23Steve_WaistLBack, 22Steve_WaistLFront, 24Steve_WaistRBack, 25Steve_WaistRFront
l13 = [order_of_markers[23], order_of_markers[22], order_of_markers[24], order_of_markers[25]]
w13 = [0.333333, 0.16666666, 0.333333, 0.16666666]
update_virtual_data("weight", l13, w13, "v_Spine4") 

#Spine5 between 2 other spine virtual markers
l14 = [virtual_markers[12], virtual_markers[13]]
w14 = [0.5, 0.5]
update_virtual_data("weight", l14, w14, "v_Spine5") 


#RLeg1 between 24Steve_WaistRBack and 34Steve_RThigh
l15 = [order_of_markers[24], order_of_markers[34]]
w15 = [0.75, 0.25]
update_virtual_data("weight", l15, w15, "v_RLeg1") 

#LLeg1 between 23Steve_WaistLBack and 26Steve_LThigh
l16 = [order_of_markers[23], order_of_markers[26]]
w16 = [0.75, 0.25]
update_virtual_data("weight", l16, w16, "v_LLeg1") 

#Spine6 between LLeg1 and RLeg1
l17 = [virtual_markers[16], virtual_markers[15]]
w17 = [0.5, 0.5]
update_virtual_data("weight", l17, w17, "v_Spine6")

#Knees 
#RLeg2 between 36Steve_RShin and 35Steve_RKneeOut
l18 = [order_of_markers[35]]
w17 = [0.0, .06, 0.0]
update_virtual_data("offset", l18, w17, "v_RLeg2")

#LLeg2 between 28Steve_LShin and 27Steve_LKneeOut
l19 = [order_of_markers[27]]
w17 = [0.0, -.06, 0.0]
update_virtual_data("offset", l19, w17, "v_LLeg2") 

#Feet 
#LAnkle between 29Steve_LAnkleOut, 33Steve_LForefootIn, and 30Steve_LHeelBack
l20 = [order_of_markers[29], order_of_markers[33], order_of_markers[30]]
w20 = [0.35, 0.375, 0.275]
update_virtual_data("weight", l20, w20, "v_LAnkle") 

#RAnkle between 37Steve_RAnkleOut, 41Steve_RForefootIn, and 38Steve_RHeelBack
l21 = [order_of_markers[37], order_of_markers[41], order_of_markers[38]]
w21 = [0.35, 0.375, 0.275]
update_virtual_data("weight", l21, w21, "v_RAnkle") 

#RFoot between 41Steve_RForefootIn, 39Steve_RForefootOut
l22 = [order_of_markers[41], order_of_markers[39]]
w22 = [0.5, 0.5]
update_virtual_data("weight", l22, w22, "v_RFoot") 

#LFoot between 33Steve_LForefootIn, 31Steve_LForefootOut
l23 = [order_of_markers[33], order_of_markers[31]]
w23 = [0.5, 0.5]
update_virtual_data("weight", l23, w23, "v_LFoot") 

#LToe between 32Steve_LToeTip, 31Steve_LForefootOut
l24 = [order_of_markers[32], order_of_markers[31]]
w24 = [0.75, 0.25]
update_virtual_data("weight", l24, w24, "v_LToe") 

#RToe between 40Steve_RToeTip, 39Steve_RForefootOut
l25 = [order_of_markers[40], order_of_markers[39]]
w25 = [0.75, 0.25]
update_virtual_data("weight", l25, w25, "v_RToe") 


#Update the location of virtual markers on each frame
def update_virtual_marker(index):
    if(v_relationship[index] is "weight"):
        center = Vector((0, 0, 0))
        weight_iter = 0
        for x in surrounding_markers[index]:
            center += x.location*weights[index][weight_iter]
            weight_iter += 1
        coord = Vector((float(center[0]), float(center[1]), float(center[2])))
    elif(v_relationship[index] is "xyz"):
        x = surrounding_markers[index][0].location[0]
        y = surrounding_markers[index][1].location[1]
        z = surrounding_markers[index][2].location[2]
        coord = Vector((x, y, z))
    else: #relationship is "offset"
        center = surrounding_markers[index][0].location
        for n in range(len(weights[index])):
            center[n] += weights[index][n]
        coord = Vector((float(center[0]), float(center[1]), float(center[2])))
    virtual_markers[index].location = coord
        
        

#-----------------------------------------------------------------------------------

#adds child bone given corresponding parent and empty
#bone tail will appear at the location of empty
def add_child_bone(bone_name, empty1, empty2):
    #Create a new bone
    new_bone = armature_data.data.edit_bones.new(bone_name)
    #Set bone's size
    new_bone.head = (0,0,0)
    new_bone.tail = (0,0.5,0)
    #Set bone's location to wheel
    new_bone.matrix = empty2.matrix_world
    #set location of bone head
    new_bone.head =  empty1.location
    #set location of bone tail
    new_bone.tail = empty2.location
    return new_bone


#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)
#Set edit mode
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#Set bones in front and show axis
armature_data.show_in_front = True
#True to show axis orientation of bones and false to hide it
armature_data.data.show_axes = False
#get armature object
def get_armature():
    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE':
            armature = ob
            break
    return armature
armature = get_armature()



#Define how Skeleton bones connect to one another
list_of_bones_order = [('bone0', virtual_markers[0], virtual_markers[3]), #v_R_Wrist to v_R_Hand
('bone1', virtual_markers[1], virtual_markers[2]), #v_L_Wrist to v_L_Hand
('bone2', virtual_markers[4], virtual_markers[1]), #v_L_Elbow to v_L_Wrist
('bone3', virtual_markers[5], virtual_markers[0]), #v_R_Elbow to v_R_Wrist
('bone4', virtual_markers[6], virtual_markers[5]), #v_R_Shoulder to v_R_Elbow 
('bone5', virtual_markers[7], virtual_markers[4]), #v_L_Shoulder to v_L_Elbow 
('bone6', virtual_markers[8], virtual_markers[7]),  #v_Chest to v_L_Shoulder
('bone7', virtual_markers[8], virtual_markers[6]), #v_Chest to v_R_Shoulder
('bone8', virtual_markers[9], virtual_markers[10]), #v_Head to v_Spine1
('bone9', virtual_markers[10], virtual_markers[11]), #v_Spine1 to v_Spine2
('bone10', virtual_markers[11], virtual_markers[12]),  #v_Spine2 to v_Spine3
('bone11', virtual_markers[12], virtual_markers[14]),  #v_Spine3 to v_Spine5
('bone12', virtual_markers[14], virtual_markers[13]),  #v_Spine5 to v_Spine4
('bone13', virtual_markers[14], virtual_markers[13]), #v_RLeg1 to v_RLeg2
('bone14', virtual_markers[13], virtual_markers[17]), #v_Spine4 to v_Spine6
('bone15', virtual_markers[15], virtual_markers[17]), #v_Spine6 to v_RLeg1
('bone16', virtual_markers[16], virtual_markers[17]), #v_Spine6 to v_LLeg1
('bone17', virtual_markers[15], virtual_markers[18]), #v_RLeg1 to v_RLeg2
('bone18', virtual_markers[16], virtual_markers[19]), #v_LLeg1 to v_LLeg2]  
('bone19', virtual_markers[19], virtual_markers[20]), #v_LLeg2 to v_LAnkle
('bone20', virtual_markers[18], virtual_markers[21]), #v_RLeg2 to v_RAnkle
('bone21', virtual_markers[21], virtual_markers[22]), #v_RAnkle to v_RFoot
('bone22', virtual_markers[20], virtual_markers[23]), #v_LAnkle to v_LFoot
('bone23', virtual_markers[23], virtual_markers[24]), #v_LFoot to v_LToe
('bone24', virtual_markers[22], virtual_markers[25])] #v_RFoot to v_RToe
        
#helper to create armature from list of tuples
def tuple_to_armature(bones):
    for bone_name, bone_head, bone_tail in bones:
        add_child_bone(bone_name, bone_head, bone_tail)
        
#create all bones for skeleton body and hands
tuple_to_armature(list_of_bones_order)

#parent heads and tails to empties
#use bone constraints 
def parent_to_empties(bone_name, head, tail):
    #enter pose mode
    bpy.ops.object.mode_set(mode='POSE')
    marker = armature.data.bones[bone_name]
    #Set marker selected
    marker.select = True
    #Set marker active
    bpy.context.object.data.bones.active = marker
    bone = bpy.context.object.pose.bones[bone_name]
    #Copy Location Pose constraint: makes the bone's head follow the given empty
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    bone.constraints["Copy Location"].target = head
    #Stretch To Pose constraint: makes the bone's tail follow the given empty
    #stretches the bones to reach the tail to that empty so head location is not affected
    bpy.ops.pose.constraint_add(type='STRETCH_TO')
    bone.constraints["Stretch To"].target = tail
    #exit pose mode
    bpy.ops.object.posemode_toggle()
    
#set parents of heads and tails for each bone 
def tuple_to_parented(bones):
    for bone_name, bone_head, bone_tail in bones:
        parent_to_empties(bone_name, bone_head, bone_tail)

#set parents of bone heads and tails
tuple_to_parented(list_of_bones_order)
#make bone display in blender viewport stick
bpy.context.object.data.display_type = 'STICK'
#don't show armature in front of mesh
bpy.context.object.show_in_front = False

#-----------------------------------------------------------------------------------
# Animate!
#find number of frames in animation

#find number of frames in file
num_frames = len(file) - 11

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = num_frames * 400
plot_force_array = []
current_skel_frame = [0]
bpy.context.scene.render.fps = 1200

                
def my_handler(scene): 
    frames_seen = 0
    #must be in pose mode to set keyframes
    bpy.ops.object.mode_set(mode='POSE')
    #keep track of current_marker
    current_marker = 0 
    #find the current frame number
    frame = scene.frame_current
    current_frame_skeleton_data = current_skel_frame[0]
    if (frame - 1) % 4 == 0:
        current_skel_frame[0] = int((frame - 1) / 4)
        #get the list of marker points from the current frame
        #markers_list = create_data_arr((frame - 1) / 400)
    markers_list = create_data_arr(current_skel_frame[0])
        #current virtual marker 
    current_virtual_marker = 0
    #iterate through list of markers in this frame
    for col in markers_list:
        if (col[0] and col[1] and col[2]):
            coord = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, float(col[2]) * 0.001))
            empty = order_of_markers[current_marker] 
            #change empty position : this is where the change in location every frame happens
            empty.location = coord
            #Set keyframes of the empty location at this frame to save the animation
            #empty.keyframe_insert(data_path='location',frame=scene.frame_current)
            #increment counter of the number marker we are currently changing
        current_marker += 1 
    for index in range(len(virtual_markers)):
        update_virtual_marker(index)
    #update force plate
    current_force_plate_arr = create_data_arr_force_plate(frame)
    #Center of pressure from data is the base of the arrow
    coord_bottom = Vector((plate_origin[0] + (float(current_force_plate_arr[2][0]))* 0.001, plate_origin[1] + (float(current_force_plate_arr[2][1]))* 0.001, plate_origin[2] + (float(current_force_plate_arr[2][2])* 0.001)))
    #force from data scaled by a number is the height of arrow 
    coord_top = Vector((coord_bottom[0] + float(current_force_plate_arr[0][0])* 0.001, coord_bottom[1] + float(current_force_plate_arr[0][1])* 0.001, coord_bottom[2] + float(current_force_plate_arr[0][2])* 0.001))
    if coord_top[2] <= 0:
        #Do not render the ring in final output
        obj_arrow.hide_set(True)
        obj_arrow.hide_render = True
        cone.hide_set(True)
        cone.hide_render = True
    else:
        #render the ring in final output
        obj_arrow.hide_set(False)
        obj_arrow.hide_render = False
        cone.hide_set(False)
        cone.hide_render = False
        #coord_top[2] *= 10
    arrow_bottom.location = coord_bottom
    arrow_top.location = coord_top
    
    

#script to create a mesh of the armature 
def CreateMesh():
    obj = get_armature()

    if obj == None:
        print( "No selection" )
    elif obj.type != 'ARMATURE':
        print( "Armature expected" )
    else:
        return processArmature( bpy.context, obj )

#Use armature to create base object
def armToMesh( arm ):
    name = arm.name + "_mesh"
    dataMesh = bpy.data.meshes.new( name + "Data" )
    mesh = bpy.data.objects.new( name, dataMesh )
    mesh.matrix_world = arm.matrix_world.copy()
    return mesh

#Make vertices and faces 
def boneGeometry( l1, l2, x, z, baseSize, l1Size, l2Size, base ):
    #make bones thinner
    x1 = x * .1 * .1
    z1 = z * .1 * .1
    
    x2 = Vector( (0, 0, 0) )
    z2 = Vector( (0, 0, 0) )

    verts = [
        l1 - x1 + z1,
        l1 + x1 + z1,
        l1 - x1 - z1,
        l1 + x1 - z1,
        l2 - x2 + z2,
        l2 + x2 + z2,
        l2 - x2 - z2,
        l2 + x2 - z2
        ] 

    faces = [
        (base+3, base+1, base+0, base+2),
        (base+6, base+4, base+5, base+7),
        (base+4, base+0, base+1, base+5),
        (base+7, base+3, base+2, base+6),
        (base+5, base+1, base+3, base+7),
        (base+6, base+2, base+0, base+4)
        ]

    return verts, faces

#Process the armature, goes through its bones and creates the mesh
def processArmature(context, arm, genVertexGroups = True):
    print("processing {0}".format(arm.name))

    #Creates the mesh object
    meshObj = armToMesh( arm )
    context.collection.objects.link( meshObj )

    verts = []
    edges = []
    faces = []
    vertexGroups = {}

    bpy.ops.object.mode_set(mode='EDIT')
    try:
        #Goes through each bone
        for editBone in arm.data.edit_bones:
            boneName = editBone.name
            print( boneName )
            poseBone = arm.pose.bones[boneName]

            #Gets edit bone informations
            editBoneHead = editBone.head
            editBoneTail = editBone.tail
            editBoneVector = editBoneTail - editBoneHead
            editBoneSize = editBoneVector.dot( editBoneVector )
            editBoneRoll = editBone.roll
            editBoneX = editBone.x_axis
            editBoneZ = editBone.z_axis
            editBoneHeadRadius = editBone.head_radius
            editBoneTailRadius = editBone.tail_radius

            #Creates the mesh data for the bone
            baseIndex = len(verts)
            baseSize = sqrt( editBoneSize )
            newVerts, newFaces = boneGeometry( editBoneHead, editBoneTail, editBoneX, editBoneZ, baseSize, editBoneHeadRadius, editBoneTailRadius, baseIndex )

            verts.extend( newVerts )
            faces.extend( newFaces )

            #Creates the weights for the vertex groups
            vertexGroups[boneName] = [(x, 1.0) for x in range(baseIndex, len(verts))]

        #Assigns the geometry to the mesh
        meshObj.data.from_pydata(verts, edges, faces)

    except:
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.object.mode_set(mode='OBJECT')
    #Assigns the vertex groups
    if genVertexGroups:
        for name1, vertexGroup in vertexGroups.items():
            groupObject = meshObj.vertex_groups.new(name = name1)
            for (index, weight) in vertexGroup:
                groupObject.add([index], weight, 'REPLACE')

    #Creates the armature modifier
    modifier = meshObj.modifiers.new('ArmatureMod', 'ARMATURE')
    modifier.object = arm
    modifier.use_bone_envelopes = False
    modifier.use_vertex_groups = True

    meshObj.data.update()

    return meshObj

mesh_obob = CreateMesh()

#-----------------------------------------------------------------------------------
# Clean up the mesh by removing duplicate vertices, make sure all faces are quads, etc

checked = set()
for selected_object in bpy.data.objects:
    if selected_object.type != 'MESH':
        continue
    meshdata = selected_object.data
    if meshdata in checked:
        continue
    else:
        checked.add(meshdata)
    bpy.context.view_layer.objects.active = selected_object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.tris_convert_to_quads()
    bpy.ops.mesh.normals_make_consistent()
    bpy.ops.object.editmode_toggle()
#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True) 

#-----------------------------------------------------------------------------------
#Assign material to skeleton bones
#material assignment
ob = mesh_obob

# Get material
mat = bpy.data.materials.get("Mesh_mat")
if mat is None:
    # create material
    print("mat was none")
    mat = bpy.data.materials.new(name="Mesh_mat")

# Assign it to object
if ob.data.materials:
    # assign to 1st material slot
    ob.data.materials[0] = mat
else:
    # no slots
    ob.data.materials.append(mat)


#Assign material to outline of mesh
mat2 = bpy.data.materials.get("mesh_outline")
if mat2 is None:
    # create material
    print("mat was none")
    mat2 = bpy.data.materials.new(name="mesh_outline")
else:
    print("mat was found")
# Assign it to object
if outline_mesh_obob.data.materials:
    # assign to 1st material slot
     outline_mesh_obob.data.materials[0] = mat2   
else:
    # no slots
    outline_mesh_obob.data.materials.append(mat2)
    
#Arrow  
mat3 = bpy.data.materials.get("walls")
if mat3 is None:
    # create material
    print("mat was none")
    mat3 = bpy.data.materials.new(name="walls")
else:
    print("mat was found")
# Assign it to object
if obj_arrow.data.materials:
    # assign to 1st material slot
     obj_arrow.data.materials[0] = mat3   
else:
    # no slots
    obj_arrow.data.materials.append(mat3)

#force plate
mat4 = bpy.data.materials.get("walls")
if mat4 is None:
    # create material
    print("mat was none")
    mat4 = bpy.data.materials.new(name="walls")
else:
    print("mat was found")
# Assign it to object
if obj_f.data.materials:
    # assign to 1st material slot
     obj_f.data.materials[0] = mat4   
else:
    # no slots
    obj_f.data.materials.append(mat4)

print("assigned materials")


#-----------------------------------------------------------------------------------
#add visible sphere meshes on each marker

for empty in order_of_markers:
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(0, 0, 0))
    sphere = bpy.context.selected_objects[0]
    sphere.parent = empty
    sphere.matrix_world.translation = empty.matrix_world.translation
    #size of sphere
    sphere.scale[0] = 0.015
    sphere.scale[1] = 0.015
    sphere.scale[2] = 0.015
    mat = bpy.data.materials.get("Material-marker")
    if sphere.data.materials:
        # assign to 1st material slot
        sphere.data.materials[0] = mat
    else:
        # no slots
        sphere.data.materials.append(mat)

#-----------------------------------------------------------------------------------
'''
#Adjust camera position / rotation
bpy.ops.object.posemode_toggle()
camera = bpy.data.objects["Camera"]
camera.location = Vector((0, 0, -60))
camera.rotation_mode = "QUATERNION"
camera.rotation_quaternion[0] = 0
camera.rotation_quaternion[1] = 20
camera.rotation_quaternion[2] = -20
camera.rotation_quaternion[3] = 0
'''

#--------------------------------------------------------------------
#append handler function
                
bpy.app.handlers.frame_change_post.clear()
#function to register custom handler
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
        
register()
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)

#-----------------------------------------------------------------------------------
#script to export animation as pngs and add info to XML file
print("Saving frames...")
scene = bpy.context.scene
#set the number of frames to output 
#iterate through all frames
for frame in range(frame_start, frame_end):
    #specify file path to the folder you want to export to
    scene.render.filepath = output_frames_folder + "/frames/" + str(frame)
    scene.frame_set(frame)
    #render frame
    bpy.ops.render.render(write_still=True)
    '''
    #add information for each frame to XML file
    child0 = SubElement(frames, 'frame' + str(frame))
    child1 = SubElement(child0, 'markers')
    child2 = SubElement(child0, 'armature')
    current_marker = 0
    #Log XML for each marker from original npy data
    for col in markers_list:
        coord = Vector((float(col[0]), float(col[1]), float(col[2])))
        empty = order_of_markers[current_marker] 
        marker_node = SubElement(child1, empty.name)
        create_node(marker_node, "Location", str(coord))
        current_marker += 1
    #Log XML for each bone's location and rotation
    for bone in bpy.data.objects['Armature'].pose.bones:
        bone_node = SubElement(child2, bone.name)
        create_node(bone_node, "Location", str(bone.location))
        create_node(bone_node, "Rotation", str(bone.rotation_quaternion))
        '''
print("finished!")