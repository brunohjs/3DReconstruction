import bpy
import sys
import mathutils
import os.path
from io_mesh_ply import import_ply
from glob import glob



#comando pra executar o script no blender
#blender --python ~/Desktop/3DReconstruction/modules/render.py outputs/wall2.ply

position = mathutils.Vector((0,0,92))
objects = list()

for i in range(3, len(sys.argv)):
    if sys.argv[i][-1] != '/':
        sys.argv[i] += '/'
    meshs = glob(sys.argv[i]+'*')
    for filename in meshs:
        if os.path.basename(filename)[-4:] == '.ply':
            name = os.path.basename(filename)[:-4]
            surface = import_ply.load_ply_mesh(filename, name)
            objects.append(bpy.data.objects.new(name, surface))
            objects[-1].location = position
            bpy.context.scene.objects.link(objects[-1])
        else:
            print('Error: file is not a .ply format file.')

#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
