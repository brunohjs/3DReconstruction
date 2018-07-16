import bpy
import sys
import mathutils
from io_mesh_ply import import_ply
import os.path

#comando pra executar o script no blender
#blender --python ~/Desktop/3DReconstruction/modules/render.py outputs/wall2.py

position = mathutils.Vector((0,0,92))

if len(sys.argv) == 5:
    name = os.path.basename(sys.argv[4])[:-4]
    surface2 = import_ply.load_ply_mesh(sys.argv[4], name)
    obj2 = bpy.data.objects.new(name, surface2)
    obj2.location = position
    bpy.context.scene.objects.link(obj2)

name = os.path.basename(sys.argv[3])[:-4]
surface1 = import_ply.load_ply_mesh(sys.argv[3], name)
obj1 = bpy.data.objects.new(name, surface1)
obj1.location = position
bpy.context.scene.objects.link(obj1)

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
