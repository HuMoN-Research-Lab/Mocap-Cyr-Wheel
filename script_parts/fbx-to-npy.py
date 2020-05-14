#exports camera info as FBX in form [[position, rotation], [position, rotation]...] as npy and as XML
#exports frames and markers in form [[x, y, z], [x, y, z]...]...] (an array of frames where each frame is array of markers [x, y, z]) as npy and as XML

import re, csv, numpy as np
import argparse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring, SubElement, Comment
from datetime import datetime
import xml.dom.minidom

def main(fbx_file_location, tsv_file_location):

    #camera info
    #List to export as npy
    list1 = []

    #Create node for XML
    def create_node(parent, name, text):
            child1 = SubElement(parent, name)
            child1.text = text

    with open(fbx_file_location, "r") as file:
        # Log info to XML file
        # create the file structure
        camera = Element('Camera_Data')

        # current date and time
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        dt_object = datetime.fromtimestamp(timestamp)
        date = SubElement(camera, "timestamp")
        date.text = str(dt_object)
        cameras = SubElement(camera, "Cameras")  
        
        for title, body in re.findall(r"(#\d* Miqus Video)\".*?{(.*?)}", file.read(), re.MULTILINE | re.DOTALL):
            translation = re.search(r"Lcl Translation.*?\"A\",([\-0-9.]+),([\-0-9.]+),([\-0-9.]+)", body, re.MULTILINE | re.DOTALL).groups()
            rotation = re.search(r"Lcl Rotation.*?\"A\",([\-0-9.]+),([\-0-9.]+),([\-0-9.]+)", body, re.MULTILINE | re.DOTALL).groups()
            list1.append([list(translation), list(rotation)])
            node = SubElement(cameras, title)
            child1 = SubElement(parent, name)
            child1.text = text
            create_node(node, "Translation", str("" + list(translation)[0] + "," +  list(translation)[1] + "," + list(translation)[2]))
            create_node(node, "Rotation", str("" + list(rotation)[0] + "," +  list(rotation)[1] + "," + list(rotation)[2])

    #save npy
    a = np.array(list1)
    np.save('cameras.npy', a)

    #raw XML file
    mydata = ET.tostring(camera, encoding="unicode")
    myfile = open("camera_output_data_raw.xml", "w")
    myfile.write(mydata)
    myfile.close() 
    print(mydata)

    #formatted human-readable XML file
    dom = xml.dom.minidom.parseString(mydata)
    pretty_xml_as_string = dom.toprettyxml()
    myfile2 = open("camera_output_data_pretty.xml", "w")
    myfile2.write(pretty_xml_as_string)
    myfile2.close()



    #frames and marker info
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
    frames = Element('Frame_Data')

    # current date and time
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    dt_object = datetime.fromtimestamp(timestamp)
    date = SubElement(frames, "timestamp")
    date.text = str(dt_object)

    with open(tsv_file_location, "r") as tsv_file:
        file = list(csv.reader(tsv_file, delimiter='\t'))
        #the data from frame 1
        frame = 0
        num_frames = int(file[0][1])
        frame_node = SubElement(frames, "Frames")
        for x in range(num_frames):
            arr = create_data_arr(x)
            list2.append(arr)
            print(arr)
            #create_node(frame_node, "Position", translation)
            #create_node(frame_node, "Rotation", rotation)
            
    #save npy
    b = np.array(list2)
    np.save('markers.npy', b)

    #raw XML file
    mydata = ET.tostring(camera, encoding="unicode")
    myfile = open(r"markers_output_data_raw.xml", "w")
    myfile.write(mydata)
    myfile.close() 

    #formatted human-readable XML file
    dom = xml.dom.minidom.parseString(mydata)
    pretty_xml_as_string = dom.toprettyxml()
    myfile2 = open(r"markers_output_data_pretty.xml", "w")
    myfile2.write(pretty_xml_as_string)
    myfile2.close()

        
    print("finished!")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('fbx_path', type=str,
                        help='fbx file path')
    parser.add_argument('tsv_path', type=str,
                        help='tsv file path')
    args = parser.parse_args()
    main(args.fbx_path, args.tsv_path)
    