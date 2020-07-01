import numpy as np, csv

import matplotlib

print(matplotlib.matplotlib_fname())
import matplotlib.pyplot as plt



#Start frame of data
frame_start = 0

#Start frame of data
frame_end = frame_start + 1

#default number of frames to output is all of them - change this value to an integer if you 
#want to output less 
#set to "all" to output all frames
num_frames_output = "all"
#Change: the path of the tsv file 
input_tsv = r"/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/WheelForcePlate.tsv"
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
    
print(force_plate_arr)

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


X_corner_pos = [353.011101* 0.001, 1295.030594* 0.001, -2.6015* 0.001]
X_corner_neg = [747.085989* 0.001, 1294.596434* 0.001, -2.6923* 0.001]
Neg_x_neg = [746.431708* 0.001, 700.785577* 0.001, -2.1361* 0.001]
pos_x_neg = [352.357* 0.001, 701.219738* 0.001, -2.0453* 0.001]


verts_f = [X_corner_pos, X_corner_neg, Neg_x_neg, pos_x_neg]
edges_f =  [(0,1),(1,2),(2,3),(3,0)]


a = [353.011101* 0.001, 1295.030594* 0.001, -2.6015* 0.001]
b = [747.085989* 0.001, 1294.596434* 0.001, -2.6923* 0.001]
c = [746.431708* 0.001, 700.785577* 0.001, -2.1361* 0.001]
d = [352.357* 0.001, 701.219738* 0.001, -2.0453* 0.001]

plate_origin =  [(a1 + b1 + c1 + d1) / 4 for a1, b1, c1, d1  in zip(a, b, c, d)]
 
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

#-----------------------------------------------------------------------------------
# Animate!
#find number of frames in animation

#find number of frames in file
num_frames = len(file) - 11


plot_force_array = []
frames_seen_arr = []
frames_seen = 0
                
while frames_seen <= 100000:
    #must be in pose mode to set keyframes
    #keep track of current_marker
    current_marker = 0 
    #find the current frame number
    '''
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
    #update force plate
    current_force_plate_arr = create_data_arr_force_plate(frames_seen)
    #Center of pressure from data is the base of the arrow
    coord_bottom = [plate_origin[0] + (float(current_force_plate_arr[2][0]))* 0.001, plate_origin[1] + (float(current_force_plate_arr[2][1]))* 0.001, plate_origin[2] + (float(current_force_plate_arr[2][2])* 0.001)]
    #force from data scaled by a number is the height of arrow 
    coord_top = [coord_bottom[0] + float(current_force_plate_arr[0][0]) * 0.1, coord_bottom[1] + float(current_force_plate_arr[0][1]) * 0.1, coord_bottom[2] + float(current_force_plate_arr[0][2])* 0.1]
    plot_force_array.append(coord_top[1])
    frames_seen_arr.append(frames_seen)
    frames_seen += 1
    print(len(frames_seen_arr))
    print(len(plot_force_array))
    if frames_seen == 100000:
        print("reached 1000!")
        matplotlib.interactive(True)
        plt.scatter(frames_seen_arr, plot_force_array)
        plt.xlabel('frame')
        plt.ylabel('force')
        plt.show()
        plt.savefig(output_frames_folder + '/figure2.png')
    print(frames_seen)
print("finished!")