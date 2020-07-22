from scipy import signal as signal
import numpy as np
import csv

import matplotlib

import matplotlib.pyplot as plt

Inputfilepath = "/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files"
cutoff = 10.0
framerate = 1200.0

colors = ['b', 'g', 'k', 'm', 'c', 'y']
colors2 = ['c', 'y', '.5', 'r']
markers = ['*', 'o']


w = float(cutoff/ (framerate/2.0))
print("w")
print(w)
header_start = 27

input_force_plate_arr = []
input_force_plate_arr.append("/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/Force_Plate_Data/WheelForcePlate0007_f_1.tsv")
input_force_plate_arr.append("/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/Force_Plate_Data/WheelForcePlate0007_f_2.tsv")
input_force_plate_arr.append("/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/Force_Plate_Data/WheelForcePlate0007_f_3.tsv")
input_force_plate_arr.append("/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/Force_Plate_Data/WheelForcePlate0007_f_4.tsv")
input_force_plate_arr.append("/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/input_tsv_files/Force_Plate_Data/WheelForcePlate0007_f_5.tsv")

'''
def create_data_arr_force_plate(frame, plate_id):
    current_row = force_file[plate_id][frame + 27]
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
'''

#an array holding all force files info
force_file = []
#hold force plate data for one frame
force_plate_arr = []
#array holding arrays of each force plate's X_corner_pos, X_corner_neg, Neg_x_neg, pos_x_neg
force_plate_positions = []

for x in range(len(input_force_plate_arr)):
    with open(input_force_plate_arr[x], "r") as tsv_file:
        force_file_temp = list(csv.reader(tsv_file, delimiter='\t'))
        new_temp_row = []
        new_temp_full = []
        for n in range(len(force_file_temp)):
            if n >= 27 and n < 108:
                counter = 0
                temp_arr = []
                for m in range(len(force_file_temp[n])):
                    if force_file_temp[n][m] is not "" and m>=2:
                        if(counter < 2):
                            temp_arr.append(float(force_file_temp[n][m]))
                            counter += 1
                        if(counter == 2):
                            counter = 0
                            temp_arr.append(float(force_file_temp[n][m]))
                            new_temp_row.append(temp_arr)
                            temp_arr = []
                new_temp_full.append(new_temp_row)
                new_temp_row = []
        #print(new_temp_full)
        filtData = np.array(new_temp_full)

        #plot original data
        plt.plot(filtData[:, 0, 1], markers[1], color = colors[x])
        plt.xlabel('frame')
        plt.ylabel('force')

        plt.savefig(Inputfilepath + '/unfiltered' + str(x) + '.png')
        amount_of_points = len(new_temp_full[0])

        for ii in range(amount_of_points):
            for kk in range(3):
                #print(w)
                b, a = signal.butter(4, w, 'low')
                #import pdb; pdb.set_trace()
                filtData[:,ii, kk] = signal.filtfilt(b, a, filtData[:,ii,kk])
        #plot filtered
        plt.plot(filtData[:, 0, 1], markers[1], color = colors[x])
        plt.xlabel('frame')
        plt.ylabel('force')
        plt.savefig(Inputfilepath + '/filtered' + str(x) + '.png')
        np.save(Inputfilepath + '/FiltFP_' + str(x) + '.npy', filtData)
       
print(force_file)
