import pcl
import numpy as np
import itertools as it
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
from modules.aux.io import log
from modules.aux.geometry import totalArea, distance, cloud2D, projectOnPlane


'Função que gera o volume a partir de uma nuvem de pontos'
def volume(pcloud):
    pcloud_2d = cloud2D(pcloud)
    triangulation = Delaunay(pcloud_2d)
    length = len(pcloud)

    front_surface = list()
    back_surface = list()
    lateral_surface = list()
    for face in triangulation.simplices:
        front_surface.append([3, face[0], face[1], face[2]])
        front_surface.append([3, length+face[0], length+face[1], length+face[2]])
    for face in triangulation.convex_hull:
        lateral_surface.append([3, face[0], length+face[0], length+face[1]])
        lateral_surface.append([3, length+face[1], face[1], face[0]])
    return front_surface+back_surface+lateral_surface


'Função principal do módulo'
def reconstructSurface(pcloud):
    log("Reconstruindo a superfície")

    pcloud_2d = cloud2D(pcloud)
    face = Delaunay(pcloud_2d)
    face = [(3, p[0], p[1], p[2]) for p in face.simplices]
    vertex = [(p[0], p[1], p[2]) for p in pcloud]

    log(" - Área total da superfície: "+str(totalArea(vertex, face)))

    return vertex, face


'Função principal do módulo'
def reconstructVolume(pcloud):
    log("Reconstruindo a superfície")

    pcloud_plane = projectOnPlane(pcloud)
    vertex = pcloud_plane + pcloud
    face = volume(pcloud)

    #log(" - Área total da superfície: "+str(totalArea(vertex, face)))

    return vertex, face