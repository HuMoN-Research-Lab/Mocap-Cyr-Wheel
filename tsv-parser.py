import bpy
import csv 
import Numpy as np
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
        if x == len(current_row) - 10:
            print(arr)
#-----------------------------------------------------------------------------------
#Create an array of marker names 
#column 9 of tsv file holds all marker names
current_row = file[9] 
name_arr = np.arange(len(current_row - 1))
for name in range(1, len(current_row)):
    name_arr.append(name)
    
print(name_arr)
    
        
#-----------------------------------------------------------------------------------
#Create empties at marker positions    
name = 0
# make sure project unity is correct for imported data
bpy.context.scene.unit_settings.length_unit = 'METERS'
#iterate through arr and create an empty object at that location for each element
for col in arr:
    coord = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, float(col[2]) * 0.001))
    bpy.ops.object.add(type='EMPTY', location=coord)  
    mt = bpy.context.active_object  
    mt.name = "Empty" + str(name)
    name += 1
    bpy.context.scene.collection.objects.link( mt )
    mt.location = coord
    mt.empty_display_size = 0.2
    #increment name of empty
    print(Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, float(col[2]) * 0.001)))
    # parse string float value into floats, create Vector, set empty position to Vector
    # multiply by .001 because original data is recorded in millimeters, but we want meters for this project
    # mt.matrix_world.translation = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, float(col[2]) * 0.001))
    