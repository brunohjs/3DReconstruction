import pcl
import numpy as np
import itertools as it
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
from modules.helpers.io import log
from modules.helpers.geometry import totalArea, distance, cloud2D, projectOnPlane
from modules.helpers.parser import parserToList


'Função que remove triângulos que possuem um lado maior que -max_distance-'
def distanceSideTriangle(mesh, pcloud, max_distance=10):
    log("Triangularizando os pontos")

    new_mesh = list()

    if not max_distance:
        max_distance = float('inf')

    for simplice in mesh:
        simplice = list(it.combinations(simplice,3))
        
        for shape in simplice:
            discart = False
            for i in range(len(shape)-1):
                for j in range(i+1, len(shape)):
                    d = distance(pcloud[shape[i]], pcloud[shape[j]])
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
        polygon_i = Polygon([vertex[faces[i][1]], vertex[faces[i][2]], vertex[faces[i][3]]]).buffer(-0.02)
        discart = False
        for j in range(i+1, len(faces)):
            polygon_j = Polygon([vertex[faces[j][1]], vertex[faces[j][2]], vertex[faces[j][3]]])
            if polygon_i.overlaps(polygon_j):
                discart = True
                break
        if not discart:
            new_faces.append(faces[i])
    return new_faces


'Função principal do módulo'
def reconstruct(point_cloud):
    log("Reconstruindo a superfície")

    pcloud_2d = cloud2D(point_cloud)
    face = Delaunay(pcloud_2d)
    face = distanceSideTriangle(face.simplices, point_cloud, False)
    
    vertex = [(p[0], p[1], p[2]) for p in point_cloud]

    log(" - Área total da superfície: "+str(totalArea(vertex, face)))

    return vertex, face
