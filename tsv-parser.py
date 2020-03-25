import bpy, bmesh, csv
from mathutils import Matrix, Vector, Euler

#script to read tsv files in blender 
 
#-----------------------------------------------------------------------------------
#open file (adjust file location)
with open(r"C:\Users\jacki\OneDrive\Desktop\blender ring\steve.tsv", "r") as tsv_file:
    file = list(csv.reader(tsv_file, delimiter='\t'))
    #the data from frame 1
    frame = 0
    
    # Create 2D array "arr" to hold all 3D coordinate info of markers
    #numerical data begins in column 11
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
    armature = bpy.data.objects["Armature.004"]
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
root_bone.matrix = bpy.data.objects.get('Steve_CyrWheel01').matrix_world
root_bone.tail = bpy.data.objects.get('Steve_CyrWheel01').location
root_bone.head =  bpy.data.objects.get('Steve_CyrWheel05').location

#Add wheel bones to armature
marker2 = add_child_bone('marker2', root_bone, bpy.data.objects.get('Steve_CyrWheel02'))
marker3 = add_child_bone('marker3', marker2, bpy.data.objects.get('Steve_CyrWheel03'))
marker4 = add_child_bone('marker4', marker3, bpy.data.objects.get('Steve_CyrWheel04'))
marker5 = add_child_bone('marker5', marker4, bpy.data.objects.get('Steve_CyrWheel05'))

#parent heads and tails to empties