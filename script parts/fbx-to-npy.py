#exports camera info as FBX in form [[position, rotation], [position, rotation]...]
#exports frames and markers in form [[x, y, z], [x, y, z]...]...] (an array of frames where each frame is array of markers [x, y, z])
import re, csv, numpy as np
import argparse

def main(fbx_file_location, tsv_file_location):

    list1 = []
    with open(fbx_file_location, "r") as file:

        for title, body in re.findall(r"(#\d* Miqus Video)\".*?{(.*?)}", file.read(), re.MULTILINE | re.DOTALL):
            print(title)
            translation = re.search(r"Lcl Translation.*?\"A\",([\-0-9.]+),([\-0-9.]+),([\-0-9.]+)", body, re.MULTILINE | re.DOTALL).groups()
            rotation = re.search(r"Lcl Rotation.*?\"A\",([\-0-9.]+),([\-0-9.]+),([\-0-9.]+)", body, re.MULTILINE | re.DOTALL).groups()
            print(f"translation: {translation}, rotation: {rotation}")
            list1.append([list(translation), list(rotation)])

        a = np.array(list1)
        np.save('cameras.npy', a)


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

    list2 = []

    with open(tsv_file_location, "r") as tsv_file:
        file = list(csv.reader(tsv_file, delimiter='\t'))
        #the data from frame 1
        frame = 0
        num_frames = int(file[0][1])
        for x in range(num_frames):
            list2.append(create_data_arr(x))
            
    b = np.array(list2)
    np.save('markers.npy', b)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('fbx_path', type=str,
                        help='fbx file path')
    parser.add_argument('tsv_path', type=str,
                        help='tsv file path')
    args = parser.parse_args()
    main(args.fbx_path, args.tsv_path)