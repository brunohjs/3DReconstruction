import pcl
import numpy as np
import itertools as it
from scipy.spatial import Delaunay
from plyfile import PlyData, PlyElement
from shapely.geometry import Polygon
from modules.aux.calc import distance
from modules.aux.files import log
from modules.aux.geometry import totalArea 


'Função que remove triângulos que possuem um lado maior que -max_distance-'
def calcDistance(mesh, max_distance=3):
    log("Triangularizando os pontos")

    new_mesh = list()

    for simplice in mesh.simplices:
        simplice = list(it.combinations(simplice,3))
        
        for shape in simplice:
            discart = False
            for i in range(len(shape)-1):
                for j in range(i+1, len(shape)):
                    d = distance(mesh.points[shape[i]], mesh.points[shape[j]])
                    if d > max_distance:
                        discart = True
                        break
                if discart:
                    break
            shape = tuple([3]+sorted(list(shape)))
            if not discart and shape not in new_mesh:
                new_mesh.append(shape)

    return new_mesh


'Filtro que remove triângulos sobrepostos'
def overlapFilter(faces, vertex):
    log("Removendo triângulos sobrepostos")

    new_faces = list()
    index_to_discart = list()

    for i in range(len(faces)-1):
        polygon_i = Polygon([vertex[faces[i][1]], vertex[faces[i][2]], vertex[faces[i][3]]]).buffer(-0.1)
        discart = False
        for j in range(i+1, len(faces)):
            polygon_j = Polygon([vertex[faces[j][1]], vertex[faces[j][2]], vertex[faces[j][3]]]).buffer(-0.1)
            if polygon_i.intersects(polygon_j):
                discart = True
                break
        if not discart:
            new_faces.append(faces[i])
    return new_faces


def reconstruct(point_cloud):
    log("Reconstruindo a superfície")

    mesh = Delaunay(point_cloud)
    mesh = calcDistance(mesh)

    point_cloud = [(p[0], p[1], p[2]) for p in point_cloud]
    #mesh = overlapFilter(mesh, point_cloud)

    vertex = np.asarray(point_cloud, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    faces = np.asarray(mesh, dtype=[('len', 'i4'), ('v1', 'i4'), ('v2', 'i4'), ('v3', 'i4')])

    print("> Área total: ",totalArea(vertex, faces))

    vertex_element = PlyElement.describe(vertex, 'vertex')
    faces_element = PlyElement.describe(faces, 'face')

    PlyData([vertex_element, faces_element], text=True).write('teste.ply')
                