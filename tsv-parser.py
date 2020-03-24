import bpy
import csv 
from mathutils import Matrix, Vector, Euler

#script to read tsv files in blender 
#adjust file location
with open(r"C:\Users\jacki\OneDrive\Desktop\blender ring\steve.tsv", "r") as tsv_file:
    file = list(csv.reader(tsv_file, delimiter='\t'))
    #the data from frame 1
    frame = 0
    currentRow = file[frame + 11]
    cols, rows = (3, int((len(currentRow) - 2) / 3))
    arr = [[None]*cols for _ in range(rows)]
    count = 0
    countTotal = 0
    countRow = 0
    #print(currentRow)
    for x in range(2, len(currentRow)):
        arr[countRow][count] = currentRow[x]
        #print(arr[countRow][count])
        count += 1
        if (count == 3):
            count = 0
            countRow += 1
        if x == len(currentRow) - 10:
            print(arr)
            
    #start by creating first empty with name empty0       
    name = 0
    #iterate through arr and create an empty object at that location for each element
    for col in arr:
        o = bpy.data.objects.new( "empty" + str(name), None )
        #increment name of empty
        name += 1
        bpy.context.scene.collection.objects.link( o )
        print(Vector((float(col[0]), float(col[1]), float(col[2]))))
        # parse string float value into floats, create Vector, set empty position to Vector
        o.matrix_world.translation = Vector((float(col[0]), float(col[1]), float(col[2])))
    