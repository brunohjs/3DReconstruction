import pcl
import numpy as np
from scipy.spatial import Delaunay
from plyfile import PlyData, PlyElement
from modules.aux.calc import distance
from modules.aux.files import log


def calcDistante(mesh, max_distance=1.2):
    log("Triangularizando os pontos")

    new_mesh = list()
    
    for shape in mesh.simplices:
        discart = False
        for i in range(len(shape)-1):
            for j in range(i+1, len(shape)):
                d = distance(mesh.points[shape[i]], mesh.points[shape[j]])
                if d > max_distance:
                    discart = True
                    break
            if discart:
                break
        if not discart:
            new_mesh.append((len(shape), shape[0], shape[1], shape[2], shape[3]))
    print(len(new_mesh))
    return new_mesh


def reconstruct(point_cloud):
    log("Reconstruindo a superfície")

    mesh = Delaunay(point_cloud)
    new_mesh = calcDistante(mesh)
    #new_mesh = [(len(p), p[0], p[1], p[2], p[3]) for p in mesh.simplices]
    new_point_cloud = [(p[0], p[1], p[2]) for p in point_cloud]
    vertex = np.asarray(new_point_cloud, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    face = np.asarray(new_mesh, dtype=[('len', 'i4'), ('v1', 'i4'), ('v2', 'i4'), ('v3', 'i4'), ('v4', 'i4')])

    vertex_element = PlyElement.describe(vertex, 'vertex')
    face_element = PlyElement.describe(face, 'face')

    PlyData([vertex_element, face_element], text=True).write('teste.ply')


