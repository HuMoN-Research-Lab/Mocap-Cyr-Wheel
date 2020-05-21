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
with open(r"/Users/jackieallex/Downloads/Mocap-Cyr-Wheel-master/tsv files/WheelForcePlate.tsv", "r") as tsv_file:
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
    #sanity check
    print(coord)
    
Steve_CyrWheel01 = bpy.data.objects.get('Steve_CyrWheel01')
Steve_CyrWheel02 = bpy.data.objects.get('Steve_CyrWheel02')
Steve_CyrWheel03 = bpy.data.objects.get('Steve_CyrWheel03')
Steve_CyrWheel04 = bpy.data.objects.get('Steve_CyrWheel04')
Steve_CyrWheel05 = bpy.data.objects.get('Steve_CyrWheel05')

order = [Steve_CyrWheel01, Steve_CyrWheel02, Steve_CyrWheel03, Steve_CyrWheel04, Steve_CyrWheel05]
#-----------------------------------------------------------------------------------
#Create armature of wheel if it is the 1st frame

#adds child bone given corresponding parent and empty
#bone tail will appear at the location of empty
def add_child_bone(bone_name, empty):
    #Create a new bone
    new_bone = armature_data.data.edit_bones.new(bone_name)
    #Set bone's size
    new_bone.head = (0,0,0)
    new_bone.tail = (0,0.5,0)
    #Set bone's location to wheel
    new_bone.matrix = empty.matrix_world
    new_bone.head =  parent_bone.location
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
root_bone = armature_data.data.edit_bones.new('bone')
#Set its orientation and size

#get armature object
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        armature = ob
        break
    
    
iter = 0
'''
#iterate through each object in this blender project
for tracker in bpy.data.objects:
    #if the object is an empty
    if tracker.type == 'EMPTY' and ("Wheel" in tracker.name):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        #Add a bone
        new_bone = armature_data.data.edit_bones.new("bone" + str(iter))
        #resize the bone
        new_bone.head = (0,0,0)
        new_bone.tail = (0,0.5,0)
        bpy.ops.object.mode_set(mode='POSE')
        marker = armature.data.bones["bone" + str(iter)]
        #Set marker selected
        marker.select = True
        #Set marker active
        bpy.context.object.data.bones.active = marker
        bone = bpy.context.object.pose.bones["bone" + str(iter)]
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        bone.constraints["Copy Location"].target = tracker
        iter += 1

bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#Add a bone
new_bone = armature_data.data.edit_bones.new("boneblah")
#resize the bone
new_bone.head = (0,0,0)
new_bone.tail = (0,0.5,0)

bpy.ops.object.mode_set(mode='POSE')
marker = armature.data.bones["bone0"]
marker.select = True
bpy.context.object.data.bones.active = marker
bone = bpy.context.object.pose.bones["bone0"]
bpy.ops.pose.constraint_add(type='TRACK_TO')
bone.constraints["Track To"].target = order[1]
bone.constraints["Track To"].up_axis = 'UP_Z'
bpy.ops.pose.constraint_add(type='COPY_ROTATION')
bpy.context.object.pose.bones["bone0"].constraints["Copy Rotation"].target = order[1]
bpy.context.object.pose.bones["bone0"].constraints["Copy Rotation"].use_x = False
bpy.context.object.pose.bones["bone0"].constraints["Copy Rotation"].use_z = False


marker = armature.data.bones["bone1"]
marker.select = True
bpy.context.object.data.bones.active = marker
bone = bpy.context.object.pose.bones["bone1"]
bpy.ops.pose.constraint_add(type='TRACK_TO')
bone.constraints["Track To"].target = order[2]
bone.constraints["Track To"].up_axis = 'UP_Z'
bpy.ops.pose.constraint_add(type='COPY_ROTATION')
bpy.context.object.pose.bones["bone1"].constraints["Copy Rotation"].target = order[2]
bpy.context.object.pose.bones["bone1"].constraints["Copy Rotation"].use_x = False
bpy.context.object.pose.bones["bone1"].constraints["Copy Rotation"].use_z = False

marker = armature.data.bones["boneblah"]
marker.select = True
bpy.context.object.data.bones.active = marker
bone = bpy.context.object.pose.bones["boneblah"]
bpy.ops.pose.constraint_add(type='COPY_LOCATION')
bone.constraints["Copy Location"].target = order[1]
bpy.ops.pose.constraint_add(type='COPY_ROTATION')
bpy.context.object.pose.bones["boneblah"].constraints["Copy Rotation"].target = armature
bpy.context.object.pose.bones["boneblah"].constraints["Copy Rotation"].subtarget = "bone1"

marker = armature.data.bones["bone2"]
marker.select = True
bpy.context.object.data.bones.active = marker
bone = bpy.context.object.pose.bones["bone2"]
bpy.ops.pose.constraint_add(type='TRACK_TO')
bone.constraints["Track To"].target = order[3]
bone.constraints["Track To"].up_axis = 'UP_Z'
bpy.ops.pose.constraint_add(type='COPY_ROTATION')
bpy.context.object.pose.bones["bone2"].constraints["Copy Rotation"].target = order[3]
bpy.context.object.pose.bones["bone2"].constraints["Copy Rotation"].use_x = False
bpy.context.object.pose.bones["bone2"].constraints["Copy Rotation"].use_z = False


marker = armature.data.bones["bone3"]
marker.select = True
bpy.context.object.data.bones.active = marker
bone = bpy.context.object.pose.bones["bone3"]
bpy.ops.pose.constraint_add(type='TRACK_TO')
bone.constraints["Track To"].target = order[4]
bone.constraints["Track To"].up_axis = 'UP_Z'
bpy.ops.pose.constraint_add(type='COPY_ROTATION')
bpy.context.object.pose.bones["bone3"].constraints["Copy Rotation"].target = order[4]
bpy.context.object.pose.bones["bone3"].constraints["Copy Rotation"].use_x = False
bpy.context.object.pose.bones["bone3"].constraints["Copy Rotation"].use_z = False

marker = armature.data.bones["bone4"]
marker.select = True
bpy.context.object.data.bones.active = marker
bone = bpy.context.object.pose.bones["bone4"]
bpy.ops.pose.constraint_add(type='TRACK_TO')
bone.constraints["Track To"].target = order[0]
bone.constraints["Track To"].up_axis = 'UP_Z'
bpy.ops.pose.constraint_add(type='COPY_ROTATION')
bpy.context.object.pose.bones["bone4"].constraints["Copy Rotation"].target = order[0]
bpy.context.object.pose.bones["bone4"].constraints["Copy Rotation"].use_x = False
bpy.context.object.pose.bones["bone4"].constraints["Copy Rotation"].use_z = False


bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

marker.select = True
bpy.context.object.data.bones.active = marker
bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.001"].object = bpy.data.objects["Steve_CyrWheel03"]
bpy.context.object.modifiers["Hook.001"].vertex_group = "empty3"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.002"].object = bpy.data.objects["Steve_CyrWheel01"]
bpy.context.object.modifiers["Hook.002"].vertex_group = "empty1"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.003"].object = bpy.data.objects["Steve_CyrWheel02"]
bpy.context.object.modifiers["Hook.003"].vertex_group = "empty2"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.004"].object = bpy.data.objects["Steve_CyrWheel04"]
bpy.context.object.modifiers["Hook.004"].vertex_group = "empty4"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.005"].object = bpy.data.objects["Steve_CyrWheel05"]
bpy.context.object.modifiers["Hook.005"].vertex_group = "empty5"
#bone structure by empties
#Root:    head = Steve_CyrWheel05, tail = Steve_CyrWheel01
#marker2: head = Steve_CyrWheel01, tail = Steve_CyrWheel02
#marker3: head = Steve_CyrWheel02, tail = Steve_CyrWheel03
#marker4: head = Steve_CyrWheel03, tail = Steve_CyrWheel04
#marker5: head = Steve_CyrWheel04, tail = Steve_CyrWheel05



'''

bpy.ops.object.mode_set(mode='EDIT', toggle=False)
mesh = bpy.data.meshes.new("myBeautifulMesh")  # add the new mesh
obj = bpy.data.objects.new("MyObject", mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

verts = [order[0].location, 
         order[1].location,
         order[2].location,
         order[3].location,
         order[4].location
         ]  # 4 verts made with XYZ coords
edges = []
faces = [[0, 1, 2, 3, 4]]

mesh.from_pydata(verts, [], faces)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')



'''
verts = [order[0].location, 
         order[1].location,
         order[2].location,
         order[3].location,
         order[4].location
         ]  # 2 verts made with XYZ coords
mesh = bpy.data.meshes.new("myBeautifulMesh")  # add a new mesh
obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh

bpy.context.collection.objects.link(obj)  # put the object into the scene (link)
#Set armature active
bpy.context.view_layer.objects.active = obj
#Set armature selected
obj.select_set(state=True)

mesh = bpy.context.object.data
bm = bmesh.new()

for v in verts:
    bm.verts.new(v)  # add a new vert

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished

bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

marker.select = True
bpy.context.object.data.bones.active = marker
bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.001"].object = bpy.data.objects["Steve_CyrWheel03"]
bpy.context.object.modifiers["Hook.001"].vertex_group = "empty3"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.002"].object = bpy.data.objects["Steve_CyrWheel01"]
bpy.context.object.modifiers["Hook.002"].vertex_group = "empty1"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.003"].object = bpy.data.objects["Steve_CyrWheel02"]
bpy.context.object.modifiers["Hook.003"].vertex_group = "empty2"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.004"].object = bpy.data.objects["Steve_CyrWheel04"]
bpy.context.object.modifiers["Hook.004"].vertex_group = "empty4"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.005"].object = bpy.data.objects["Steve_CyrWheel05"]
bpy.context.object.modifiers["Hook.005"].vertex_group = "empty5"
'''

for obj in bpy.context.scene.objects:
    if obj.name.startswith("Torus"):
        ring = obj
    
### set the relation to foot
ring.parent = obj
ring.parent_type = 'VERTEX_3'
n = len(obj.data.vertices)
ring.parent_vertices = range(1, 4)
#-----------------------------------------------------------------------------------
# Animate!
#find number of frames in animation


num_frames = len(file) - 11

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = num_frames 

#create a new handler to change empty positions every frame
def my_handler(scene): 
    frames_seen = 0
    #Set armature active
    bpy.context.view_layer.objects.active = armature_data
    #Set armature selected
    armature_data.select_set(state=True)
    #must be in pose mode to set keyframes
    bpy.ops.object.mode_set(mode='POSE')
    #keep track of current_marker
    current_marker = 0 
    #find the current frame number
    frame = scene.frame_current
    print("frame")
    print(frame)
    #get the list of marker points from the current frame
    markers_list = create_data_arr(frame - 1)
    #iterate through list of markers in this frame
    print("plane")
    for obj in bpy.context.scene.objects:
        if obj.name.startswith("Torus"):
            mesh = obj
    print(mesh.matrix_world.to_translation())
    print(mesh.matrix_world.to_euler())
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
                
#function to register custom handler
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
        
register()
