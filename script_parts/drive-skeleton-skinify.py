import numpy as np, bpy, csv
from mathutils import Matrix, Vector, Euler
from math import *
import time


#To do 
# - connect edges between connected vertices --done
# - apply skinify to it
# - create virtual markers at estimated locations
# - create rigged skeleton for those virtual markers
# - animate virtual markers by recalculating their positions at each frame


#script to read tsv files in blender

# Create 2D array "arr" to hold all 3D coordinate info of markers
#numerical data begins in column 11
def create_data_arr(frame):
    current_row = file[frame + 11]
    cols, rows = (3, int((len(current_row) - 2) / 3))
    arr = [[None]*cols for _ in range(rows)]
    count = 0
    count_total = 0
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
with open(r"/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/SteveAIMModel0002.tsv", "r") as tsv_file:
    file = list(csv.reader(tsv_file, delimiter='\t'))
    #the data from frame 1
    frame = 0
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
    bpy.context.scene.collection.objects.link( mt )
    mt.location = coord
    mt.empty_display_size = 0.01
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

#create a plane mesh connecting the wheel markers
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
mesh = bpy.data.meshes.new("myBeautifulMesh")  # add the new mesh
obj = bpy.data.objects.new("MyObject", mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

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

 # verts made with XYZ coords
verts = []
faces = []
iter = 0;
for x in order_of_markers:
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
mesh.from_pydata(verts, edges, faces)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
#Set origin of the plane to its median center
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


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
        
    

#--------------------------------------------------------------
#Virtual Markers!

#Create virtual markers takes in a string name and a list of marker s that influence it and weights
def create_marker(name, markers, weighted):
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
        create_marker(vname, surrounding, vweights)
    else :
        create_marker_xyz(vname, surrounding)
    
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
l4 = [virtual_markers[1], order_of_markers[7], order_of_markers[7]]
w4 = []
update_virtual_data("xyz", l4, w4, "v_L_Elbow")

#X is v_R_Wrist (virtual_markers[0], 
#Y is 14Steve_RElbowOut (order_of_markers[14]),
#and Z is 14Steve_RElbowOut (order_of_markers[14])
l5 = [virtual_markers[0], order_of_markers[14], order_of_markers[14]]
w5 = []
update_virtual_data("xyz", l5, w5, "v_R_Elbow") 

#Shoulders
#between 11Steve_RShoulderTop and 12Steve_RShoulderBack
l6 = [order_of_markers[11], order_of_markers[12]]
w6 = [0.9, 0.1]
update_virtual_data("weight", l6, w6, "v_R_Shoulder") 

#between 4Steve_LShoulderTop and 5Steve_LShoulderBack
l7 = [order_of_markers[4], order_of_markers[5]]
w7 = [0.9, 0.1]
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

#Leg2
#RLeg1 between 24Steve_WaistRBack and 34Steve_RThigh
l15 = [order_of_markers[24], order_of_markers[34]]
w15 = [0.75, 0.25]
update_virtual_data("weight", l15, w15, "v_RLeg1") 

#LLeg1 between 23Steve_WaistLBack and 26Steve_LThigh
l16 = [order_of_markers[24], order_of_markers[34]]
w16 = [0.75, 0.25]
update_virtual_data("weight", l16, w16, "v_LLeg1") 

#Spine6 between Spine5 and RLeg1
l17 = [virtual_markers[14], virtual_markers[14], virtual_markers[15]]
w17 = []
update_virtual_data("xyz", l17, w17, "v_Spine6")

#RLeg2 between 36Steve_RShin and 35Steve_RKneeOut
l18 = [order_of_markers[35], order_of_markers[36], order_of_markers[35]]
w18 = []
update_virtual_data("xyz", l18, w18, "v_RLeg2")

#27Steve_LKneeOut

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

#Update the location of virtual markers on each frame
def update_virtual_marker(index):
    if(v_relationship[index] is "weight"):
        center = Vector((0, 0, 0))
        weight_iter = 0
        for x in surrounding_markers[index]:
            center += x.location*weights[index][weight_iter]
            weight_iter += 1
        coord = Vector((float(center[0]), float(center[1]), float(center[2])))
        virtual_markers[index].location = coord
    else:
        x = surrounding_markers[index][0].location[0]
        y = surrounding_markers[index][1].location[1]
        z = surrounding_markers[index][2].location[2]
        coord = Vector((x, y, z))
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


#bone structure by empties
#Root:    head = Steve_CyrWheel05, tail = Steve_CyrWheel01
#marker2: head = Steve_CyrWheel01, tail = Steve_CyrWheel02
#marker3: head = Steve_CyrWheel02, tail = Steve_CyrWheel03
#marker4: head = Steve_CyrWheel03, tail = Steve_CyrWheel04
#marker5: head = Steve_CyrWheel04, tail = Steve_CyrWheel05


 
#bone structure by empties
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_pose_25.png
#bone0: head = 1, tail = 3
#bone1: head = 3, tail = 2
#bone2: head = 3, tail = 2
#bone3: head = 12, tail = 13
#bone4: head = 13, tail = 14
#bone5: head = 14, tail = 21
#bone6: head = 14, tail = 19
#bone7: head = 19, tail = 20
#bone8: head = 8, tail = 9
#bone9: head = 9, tail = 10
#bone10: head = 10, tail = 11
#bone11: head = 11, tail = 24
#bone12: head = 11, tail = 22
#bone13: head = 22, tail = 23
#bone14: head = 1, tail = 5
#bone15: head = 5, tail = 6
#bone16: head = 6, tail = 7
#bone17: head = 1, tail = 2
#bone18: head = 2, tail = 3
#bone19: head = 3, tail = 4
#bone20: head = 0, tail = 16
#bone21: head = 16, tail = 18
#bone22: head = 0, tail = 15
#bone23: head = 15, tail = 17

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
('bone16', virtual_markers[16], virtual_markers[17])] #v_Spine6 to v_LLeg1
        
        
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

tuple_to_parented(list_of_bones_order)
bpy.context.object.data.display_type = 'STICK'


#-----------------------------------------------------------------------------------
# Animate!
#find number of frames in animation


num_frames = len(file) - 11

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = num_frames 
        
                
def my_handler(scene): 
    frames_seen = 0
    #must be in pose mode to set keyframes
    bpy.ops.object.mode_set(mode='POSE')
    #keep track of current_marker
    current_marker = 0 
    #find the current frame number
    frame = scene.frame_current
    #get the list of marker points from the current frame
    markers_list = create_data_arr(frame - 1)
    #current virtual marker 
    current_virtual_marker = 0
    #iterate through list of markers in this frame
    for col in markers_list:
        if (col[0] and col[1] and col[2]):
            coord = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, float(col[2]) * 0.001))
            empty = order_of_markers[current_marker] 
            #change empty position : this is where the change in location every frame happens
            if (col[0] is not '0.000') and (col[1] is not '0.000') and (col[2] is not '0.000'):
                empty.location = coord
            #Set keyframes of the empty location at this frame to save the animation
            #empty.keyframe_insert(data_path='location',frame=scene.frame_current)
            #increment counter of the number marker we are currently changing
        current_marker += 1 
    for index in range(len(virtual_markers)):
        update_virtual_marker(index)
        
        '''
        if(current_marker == len(markers_list)):
            frames_seen += 1
            bpy.ops.pose.visual_transform_apply()
            #bone.keyframe_insert(data_path = 'location')
            if bone.rotation_mode == "QUATERNION":
                #bone.keyframe_insert(data_path = 'rotation_quaternion')
            else:
                #bone.keyframe_insert(data_path = 'rotation_euler')
            #bone.keyframe_insert(data_path = 'scale')

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
    x1 = x * baseSize * l1Size 
    z1 = z * baseSize * l1Size
    
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
armature_data.select_set(state=True) '''
                
bpy.app.handlers.frame_change_post.clear()
#function to register custom handler
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
        
register()
