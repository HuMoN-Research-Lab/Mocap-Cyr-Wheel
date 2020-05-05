import bpy, bmesh, csv
from mathutils import Matrix, Vector, Euler

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
with open(r"/Users/jackieallex/Downloads/Mocap-Cyr-Wheel-master/tsv files/Handstands0009.tsv", "r") as tsv_file:
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
    mt.empty_display_size = 0.2
    order_of_markers.append(mt)
    
#-----------------------------------------------------------------------------------
#Create armature of wheel if it is the 1st frame

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
#Set edit mode
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#Set bones In front and show axis
armature_data.show_in_front = False
armature_data.data.show_axes = False

#get armature object
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        armature = ob
        break


#bone structure by empties
#Root:    head = Steve_CyrWheel05, tail = Steve_CyrWheel01
#marker2: head = Steve_CyrWheel01, tail = Steve_CyrWheel02
#marker3: head = Steve_CyrWheel02, tail = Steve_CyrWheel03
#marker4: head = Steve_CyrWheel03, tail = Steve_CyrWheel04
#marker5: head = Steve_CyrWheel04, tail = Steve_CyrWheel05

#parent heads and tails to empties
#use bone constraints 
def parent_to_empties(bone_name, head, tail):
    #enter pose mode
    bpy.ops.object.posemode_toggle()
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
    

'''
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
'''

 
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

list_of_bones_order = [('bone0', order_of_markers[1], order_of_markers[3]),
        ('bone1', order_of_markers[3], order_of_markers[0]),
        ('bone2', order_of_markers[3], order_of_markers[2]),
        ('bone3', order_of_markers[19], order_of_markers[18]),
        ('bone4', order_of_markers[18], order_of_markers[4]),
        ('bone5', order_of_markers[4], order_of_markers[7]),
        ('bone6', order_of_markers[7], order_of_markers[8]),
        ('bone7', order_of_markers[18], order_of_markers[11]),
        ('bone8', order_of_markers[11], order_of_markers[14]),
        ('bone9', order_of_markers[14], order_of_markers[15]),
        ('bone10', order_of_markers[22], order_of_markers[26]),
        ('bone11', order_of_markers[26], order_of_markers[27]),
        ('bone12', order_of_markers[27], order_of_markers[28]),
        ('bone13', order_of_markers[28], order_of_markers[29]),
        ('bone14', order_of_markers[29], order_of_markers[31]),
        ('bone15', order_of_markers[29], order_of_markers[32]),
        ('bone16', order_of_markers[29], order_of_markers[33]),
        ('bone17', order_of_markers[25], order_of_markers[34]),
        ('bone18', order_of_markers[34], order_of_markers[35]),
        ('bone19', order_of_markers[35], order_of_markers[36]),
        ('bone20', order_of_markers[36], order_of_markers[37]),
        ('bone21', order_of_markers[37], order_of_markers[41]),
        ('bone22', order_of_markers[37], order_of_markers[39]), 
        ('bone23', order_of_markers[12], order_of_markers[13]),
        ('bone24', order_of_markers[13], order_of_markers[14]),
        ('bone25', order_of_markers[15], order_of_markers[17]),
        #('bone26', order_of_markers[37], order_of_markers[40]),
        ('bone27', order_of_markers[19], order_of_markers[5]),
        ('bone28', order_of_markers[5], order_of_markers[6]),
        ('bone29', order_of_markers[6], order_of_markers[7]),
        ('bone30', order_of_markers[8], order_of_markers[9]),
        ('bone31', order_of_markers[19], order_of_markers[18]),
        ('bone32', order_of_markers[18], order_of_markers[20]),
        ('bone33', order_of_markers[18], order_of_markers[21]),
        ('bone34', order_of_markers[20], order_of_markers[23]),
        ('bone35', order_of_markers[21], order_of_markers[24]),
        ('bone36', order_of_markers[23], order_of_markers[22]),
        ('bone37', order_of_markers[24], order_of_markers[25]),
        ('bone38', order_of_markers[22], order_of_markers[25]),
        ('bone39', order_of_markers[3], order_of_markers[18]),
        ('bone40', order_of_markers[29], order_of_markers[30]),
        ('bone41', order_of_markers[37], order_of_markers[38]),
        ('bone42', order_of_markers[18], order_of_markers[22]),
        ('bone43', order_of_markers[18], order_of_markers[25]),
        ('bone44', order_of_markers[23], order_of_markers[27]),
        ('bone45', order_of_markers[24], order_of_markers[35]),
        ('bone46', order_of_markers[12], order_of_markers[19]),
        ('bone47', order_of_markers[27], order_of_markers[30]),
        ('bone48', order_of_markers[35], order_of_markers[38]),
        ('bone49', order_of_markers[8], order_of_markers[10])]
        
        
#helper to create armature from list of tuples
def tuple_to_armature(bones):
    for bone_name, bone_head, bone_tail in bones:
        add_child_bone(bone_name, bone_head, bone_tail)
        
#create all bones for skeleton body and hands
tuple_to_armature(list_of_bones_order)


#set parents of heads and tails for each bone 
def tuple_to_parented(bones):
    for bone_name, bone_head, bone_tail in bones:
        parent_to_empties(bone_name, bone_head, bone_tail)

tuple_to_parented(list_of_bones_order)

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
        if(current_marker == len(markers_list)):
            frames_seen += 1
            bpy.ops.pose.visual_transform_apply()
            bone.keyframe_insert(data_path = 'location')
            if bone.rotation_mode == "QUATERNION":
                bone.keyframe_insert(data_path = 'rotation_quaternion')
            else:
                bone.keyframe_insert(data_path = 'rotation_euler')
            #bone.keyframe_insert(data_path = 'scale')
                
                
bpy.app.handlers.frame_change_post.clear()
#function to register custom handler
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
        
register()
