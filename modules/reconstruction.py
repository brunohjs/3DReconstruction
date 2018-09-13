import pcl
import numpy as np
import itertools as it
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
from modules.aux.io import log
from modules.aux.parser import parseToList
from modules.aux.geometry import totalArea, distance, getMaxValAxis


'Função que transforma a nuvem de pontos em 2D'
def cloud2D(pcloud, plane='yz'):
    pcloud = parseToList(pcloud)
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
def volume(pcloud, with_frontal=True):
    pcloud_2d = cloud2D(pcloud)
    triangulation = Delaunay(pcloud_2d)
    length = len(pcloud)

    back_surface = list()
    frontal_surface = list()
    lateral_surface = list()
    for face in triangulation.simplices:
        back_surface.append([3, face[0], face[1], face[2]])
        frontal_surface.append([3, length+face[0], length+face[1], length+face[2]])
    for face in triangulation.convex_hull:
        lateral_surface.append([3, face[0], length+face[0], length+face[1]])
        lateral_surface.append([3, length+face[1], face[1], face[0]])
    if with_frontal:
        return frontal_surface+back_surface+lateral_surface
    else:
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
def reconstructVolume(pcloud, depth=None, with_frontal=True):
    log("Reconstruindo a superfície")

    pcloud = parseToList(pcloud)
    if not depth:
        depth = getMaxValAxis(pcloud)
    pcloud_plane = projectOnPlane(pcloud, depth)
    vertex = pcloud_plane + pcloud
    face = volume(pcloud, with_frontal)

    #log(" - Área total da superfície: "+str(totalArea(vertex, face)))
    return vertex, face


def removeFrontalSurface(pcloud, depth=None):
    pcloud = parseToList(pcloud)
    if not depth:
        depth = getMaxValAxis(pcloud)
    pcloud_plane = projectOnPlane(pcloud, depth)
    face = volume(pcloud)

    pcloud_2d = cloud2D(pcloud)
    triangulation = Delaunay(pcloud_2d)
    length = len(pcloud)
    print(triangulation.convex_hull)
    
    back_surface = list()
    frontal_surface = list()
    lateral_surface = list()
    for face in triangulation.simplices:
        back_surface.append([3, face[0], face[1], face[2]])
        frontal_surface.append([3, length+face[0], length+face[1], length+face[2]])
    for face in triangulation.convex_hull:
        lateral_surface.append([3, face[0], length+face[0], length+face[1]])
        lateral_surface.append([3, length+face[1], face[1], face[0]])
    return 
    

    

