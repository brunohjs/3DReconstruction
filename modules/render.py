import bpy
import sys

#bpy.ops.import_mesh.ply(filepath=sys.argv[4])
bpy.ops.import_mesh.ply(filepath=sys.argv[3])
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')