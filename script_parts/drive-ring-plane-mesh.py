import bpy, bmesh, csv
import numpy as np
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

#all of the wheel markers
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

#create a plane mesh connecting the wheel markers
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
mesh = bpy.data.meshes.new("myBeautifulMesh")  # add the new mesh
obj = bpy.data.objects.new("MyObject", mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

 # 5 verts made with XYZ coords
verts = [order[0].location, 
         order[1].location,
         order[2].location,
         order[3].location,
         order[4].location
         ] 
edges = []
faces = [[0, 1, 2, 3, 4]]

#Create the mesh with the vertices and faces
mesh.from_pydata(verts, [], faces)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
#Set origin of the plane to its median center
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')


#Create vertex groups, one for each vertex
vg = obj.vertex_groups.new(name="group0")
vg.add([0], 1, "ADD")

vg = obj.vertex_groups.new(name="group1")
vg.add([1], 1, "ADD")

vg = obj.vertex_groups.new(name="group2")
vg.add([2], 1, "ADD")

vg = obj.vertex_groups.new(name="group3")
vg.add([3], 1, "ADD")

vg = obj.vertex_groups.new(name="group4")
vg.add([4], 1, "ADD")

for x in bpy.context.scene.objects:
        if x.name.startswith("Torus"):
            ring = x

for y in bpy.context.scene.objects:
        if y.name.startswith("MyObject_copy"):
            copy = y


bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
'''
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#bpy.ops.transform.rotate(value=0, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='VIEW', orient_matrix=((0.345287, -0.938497, -6.07222e-07), (0.159741, 0.0587715, -0.985408), (-0.924803, -0.340248, -0.170209)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
obj.location = copy.location
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

'''
### set the relation to foot
ring.parent = obj
ring.parent_type = 'VERTEX_3'
n = len(obj.data.vertices)
ring.parent_vertices = range(1, 4)

'''
location_array = [[order[0].location[0], order[0].location[1], order[0].location[2]], 
[order[1].location[0], order[1].location[1], order[1].location[2]], 
[order[2].location[0], order[2].location[1], order[2].location[2]],
[order[3].location[0], order[3].location[1], order[3].location[2]],
[order[4].location[0], order[4].location[1], order[4].location[2]]]
data = np.array(location_array)
new_location = np.average(data, axis=0)
new_location_vector = Vector((new_location[0], new_location[1], new_location[2]))

# Convert local coorinates to world coordinates before assignment
obj.data.vertices[0].co.xyz = order[0].matrix_world.to_translation()
obj.data.vertices[1].co.xyz = order[1].matrix_world.to_translation()
obj.data.vertices[2].co.xyz = order[2].matrix_world.to_translation()
obj.data.vertices[3].co.xyz = order[3].matrix_world.to_translation()
obj.data.vertices[4].co.xyz = order[4].matrix_world.to_translation()
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')


obj.location = new_location_vector
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

'''
bpy.context.view_layer.objects.active = ring
ring.select_set(state=True)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook"].object = bpy.data.objects["Steve_CyrWheel01"]
bpy.context.object.modifiers["Hook"].vertex_group = "group0"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.001"].object = bpy.data.objects["Steve_CyrWheel02"]
bpy.context.object.modifiers["Hook.001"].vertex_group = "group1"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.002"].object = bpy.data.objects["Steve_CyrWheel03"]
bpy.context.object.modifiers["Hook.002"].vertex_group = "group2"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.003"].object = bpy.data.objects["Steve_CyrWheel04"]
bpy.context.object.modifiers["Hook.003"].vertex_group = "group3"

bpy.ops.object.modifier_add(type='HOOK')
bpy.context.object.modifiers["Hook.004"].object = bpy.data.objects["Steve_CyrWheel05"]
bpy.context.object.modifiers["Hook.004"].vertex_group = "group4"

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