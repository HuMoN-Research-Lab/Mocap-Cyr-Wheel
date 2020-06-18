import bpy
import time

#frame_start = frame_start
frame_start = 15947
#frame_end = scene.frame_end + 1
frame_end = 15953

#script to export animation as pngs
scene = bpy.context.scene
for frame in range(frame_start, frame_end):
    #specify file path to the folder you want to export to
    scene.render.filepath = "/Users/jackieallex/Downloads/Mocap-Cyr-Wheel/frame/" + str(frame).zfill(4)
    scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    time.sleep(3)

print("finished!")