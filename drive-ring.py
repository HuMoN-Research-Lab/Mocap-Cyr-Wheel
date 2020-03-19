# script to drive a cyr wheel mesh with x, y, z marker positions 
import bpy
from bpy import context

obj = context.object
bpy.ops.object.mode_set(mode='EDIT')

#iterate through bones and manipulate positions
for bone in obj.data.edit_bones:
    bone.head.y += 1.0
    bone.tail.y += 1.0
         
bpy.ops.object.mode_set(mode='OBJECT')
