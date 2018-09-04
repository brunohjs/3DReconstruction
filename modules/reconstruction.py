import pcl
import numpy as np
import itertools as it
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
from modules.aux.io import log
from modules.aux.parser import parserToList
from modules.aux.geometry import totalArea, distance, getMaxValAxis


'Função que transforma a nuvem de pontos em 2D'
def cloud2D(pcloud, plane='yz'):
    pcloud = parserToList(pcloud)
    new_pcloud = list()
    if 'x' not in plane:
        for point in pcloud:
            new_pcloud.append([point[1], point[2]])
    elif 'y' not in plane:
        for point in pcloud:
            new_pcloud.append([point[0], point[2]])
    elif 'z' not in plane:
        for point in pcloud:
            new_pcloud.append([point[0], point[1]])
    return new_pcloud


'Projeta a nuvem de pontos em um plano'
def projectOnPlane(pcloud, dist, plane='yz'):
    new_pcloud = list()
    if 'x' not in plane:
        for point in pcloud:
            new_pcloud.append([dist, point[1], point[2]])
    elif 'y' not in plane:
        for point in pcloud:
            new_pcloud.append([point[0], dist, point[2]])
    elif 'z' not in plane:
        for point in pcloud:
            new_pcloud.append([point[0], point[1], dist])
    return new_pcloud


'Função que gera o volume a partir de uma nuvem de pontos'
def volume(pcloud):
    pcloud_2d = cloud2D(pcloud)
    triangulation = Delaunay(pcloud_2d)
    length = len(pcloud)

    back_surface = list()
    lateral_surface = list()
    for face in triangulation.simplices:
        back_surface.append([3, face[0], face[1], face[2]])
        back_surface.append([3, length+face[0], length+face[1], length+face[2]])
    for face in triangulation.convex_hull:
        lateral_surface.append([3, face[0], length+face[0], length+face[1]])
        lateral_surface.append([3, length+face[1], face[1], face[0]])
    return back_surface+lateral_surface


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
def reconstructVolume(pcloud, depth=None, dist=5):
    log("Reconstruindo a superfície")

    pcloud = parserToList(pcloud)
    if not depth:
        depth = getMaxValAxis(pcloud) + dist
    pcloud_plane = projectOnPlane(pcloud, depth)
    vertex = pcloud_plane + pcloud
    face = volume(pcloud)

    #log(" - Área total da superfície: "+str(totalArea(vertex, face)))

    return vertex, face