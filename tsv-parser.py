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
with open(r"C:\Users\jacki\OneDrive\Desktop\blender ring\steve.tsv", "r") as tsv_file:
    file = list(csv.reader(tsv_file, delimiter='\t'))
    #the data from frame 1
    frame = 0
    arr = create_data_arr(frame)
    

            
#-----------------------------------------------------------------------------------
#Create an array of marker names 
#column 9 of tsv file holds all marker names
current_row = file[9] 
print(current_row)
name_arr = []
for index in range(1, len(current_row)):
    name_arr.append(current_row[index])
        
#-----------------------------------------------------------------------------------
#Create empties at marker positions    
name = 0
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
    #sanity check
    print(coord)
    
Steve_CyrWheel01 = bpy.data.objects.get('Steve_CyrWheel01')
Steve_CyrWheel02 = bpy.data.objects.get('Steve_CyrWheel02')
Steve_CyrWheel03 = bpy.data.objects.get('Steve_CyrWheel03')
Steve_CyrWheel04 = bpy.data.objects.get('Steve_CyrWheel04')
Steve_CyrWheel05 = bpy.data.objects.get('Steve_CyrWheel05')
#-----------------------------------------------------------------------------------
#Create armature of wheel if it is the 1st frame

#adds child bone given corresponding parent and empty
#bone tail will appear at the location of empty
def add_child_bone(bone_name, parent_bone, empty):
    #Create a new bone
    new_bone = armature_data.data.edit_bones.new(bone_name)
    #Set bone's size
    new_bone.head = (0,0,0)
    new_bone.tail = (0,0.5,0)
    #Set bone's parent
    new_bone.parent = parent_bone
    #Set bone's location to wheel
    new_bone.matrix = empty.matrix_world
    new_bone.head =  parent_bone.tail
    new_bone.tail = empty.location
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
armature_data.show_in_front = True
armature_data.data.show_axes = True

#Add root bone
root_bone = armature_data.data.edit_bones.new('Root')
#Set its orientation and size
root_bone.head = (0,0,0)
root_bone.tail = (0,0.5,0)
#Set its location 
root_bone.matrix = Steve_CyrWheel01.matrix_world
root_bone.tail = Steve_CyrWheel01.location
root_bone.head =  Steve_CyrWheel05.location

#get armature object
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        armature = ob
        break

#Add wheel bones to armature
marker2 = add_child_bone('marker2', root_bone, Steve_CyrWheel02)
marker3 = add_child_bone('marker3', marker2, Steve_CyrWheel03)
marker4 = add_child_bone('marker4', marker3, Steve_CyrWheel04)
marker5 = add_child_bone('marker5', marker4, Steve_CyrWheel05)

#bone structure by empties
#Root:    head = Steve_CyrWheel05, tail = Steve_CyrWheel01
#marker2: head = Steve_CyrWheel01, tail = Steve_CyrWheel02
#marker3: head = Steve_CyrWheel02, tail = Steve_CyrWheel03
#marker4: head = Steve_CyrWheel03, tail = Steve_CyrWheel04
#marker5: head = Steve_CyrWheel04, tail = Steve_CyrWheel05

#parent heads and tails to empties
#use bone constraints 
def parent_to_empties(bone_name, head, tail):
    bpy.ops.object.posemode_toggle()
    #Armature name is "Armature.004"
    marker = armature.data.bones[bone_name]
    #Set marker selected
    marker.select = True
    #Set marker active
    bpy.context.object.data.bones.active = marker
    bone = bpy.context.object.pose.bones[bone_name]
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    bone.constraints["Copy Location"].target = head
    bpy.ops.pose.constraint_add(type='STRETCH_TO')
    bone.constraints["Stretch To"].target = tail
    bpy.ops.object.posemode_toggle()
    
#set parents of heads and tails for each bone 
parent_to_empties("Root", Steve_CyrWheel05, Steve_CyrWheel01)
parent_to_empties("marker2", Steve_CyrWheel01, Steve_CyrWheel02)
parent_to_empties("marker3", Steve_CyrWheel02, Steve_CyrWheel03)
parent_to_empties("marker4", Steve_CyrWheel03, Steve_CyrWheel04)
parent_to_empties("marker5", Steve_CyrWheel04, Steve_CyrWheel05)
 
#-----------------------------------------------------------------------------------
# Animate!
#find number of frames in animation
num_frames = len(file)
    
#create a new handler to change empty positions every frame
def my_handler(scene):
    print("Frame Change", scene.frame_current)
    #val = scene.objects['Cube'].location.x
    #scene.objects['Sphere'].location.y = val + 1.6

#register handler
def register():
    bpy.app.handlers.frame_change_post.append(my_handler)

#unregister handler
#def unregister():
    #bpy.app.handlers.frame_change_post.remove(my_handler)
    
    #once frame number hits max, unregister
    #read data from each frame 
    #starting after frame 0, change position of empties on each frame 
    #persistent handler?
    #test
    
register()
