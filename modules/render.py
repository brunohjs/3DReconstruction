import bpy
import sys
import mathutils
from io_mesh_ply import import_ply
from io_pcd import *
import os.path


#comando pra executar o script no blender
#blender --python ~/Desktop/3DReconstruction/modules/render.py outputs/wall2.ply

position = mathutils.Vector((0,0,92))
objects = list()

for i in range(3, len(sys.argv)):
    name = os.path.basename(sys.argv[i])[:-4]
    surface = import_ply.load_ply_mesh(sys.argv[i], name)
    objects.append(bpy.data.objects.new(name, surface))
    objects[-1].location = position
    bpy.context.scene.objects.link(objects[-1])

#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
