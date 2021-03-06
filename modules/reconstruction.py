import pcl
import numpy as np
import itertools as it
from scipy.spatial import Delaunay
from pymesh.meshio import form_mesh
from pymesh import separate_mesh

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
def generateVolume(pcloud, with_frontal=True, with_back=False):
    pcloud_2d = cloud2D(pcloud)
    triangulation = Delaunay(pcloud_2d)
    length = len(pcloud)

    back_surface = list()
    frontal_surface = list()
    lateral_surface = list()
    for face in triangulation.simplices:
        back_surface.append([face[0], face[1], face[2]])
        frontal_surface.append([length+face[0], length+face[1], length+face[2]])
    for face in triangulation.convex_hull:
        lateral_surface.append([face[0], length+face[0], length+face[1]])
        lateral_surface.append([length+face[1], face[1], face[0]])
    if with_frontal and with_back:
        return frontal_surface+back_surface+lateral_surface
    elif with_frontal:
        return frontal_surface+lateral_surface
    else:
        return back_surface+lateral_surface


'Função principal do módulo'
def reconstructSurface(pcloud):
    log("Reconstruindo a superfície")

    pcloud_2d = cloud2D(pcloud)
    face = Delaunay(pcloud_2d)
    vertex = [(p[0], p[1], p[2]) for p in pcloud]
    face = [(p[0], p[1], p[2]) for p in face.simplices]
    vertex, face = separate(vertex, face)

    log(" - Área total da superfície: "+str(totalArea(vertex, face)))
    return vertex, face


'Função principal do módulo'
def reconstructVolume(pcloud, depth=None, with_frontal=True, with_back=True):
    log("Reconstruindo a superfície")

    pcloud = parseToList(pcloud)
    if not depth:
        depth = getMaxValAxis(pcloud)
    pcloud_plane = projectOnPlane(pcloud, depth)
    vertex = pcloud_plane + pcloud
    face = generateVolume(pcloud, with_frontal, with_back)

    #log(" - Área total da superfície: "+str(totalArea(vertex, face)))
    return vertex, face
    

'Função que encontra os 4 pontos posteriores nas duas nuvens'
def similarBackPoints(pcloud1, pcloud2):
    pcloud1 = parseToList(pcloud1)
    pcloud2 = parseToList(pcloud2)
    INF = float('inf')
    y_min = INF
    y_max = -INF
    z_min = INF
    z_max = -INF
    x_max = -INF
    for point in pcloud1:
        if x_max < point[0]:
            x_max = point[0]
        if z_min > point[2]:
            z_min = point[2]
        if z_max < point[2]:
            z_max = point[2]  
        if y_min > point[1]:
            y_min = point[1]
        if y_max < point[1]:
            y_max = point[1]
    for point in pcloud2:
        if x_max < point[0]:
            x_max = point[0]
        if z_min > point[2]:
            z_min = point[2]
        if z_max < point[2]:
            z_max = point[2]  
        if y_min > point[1]:
            y_min = point[1]
        if y_max < point[1]:
            y_max = point[1]

    return [[x_max, y_min, z_min], 
        [x_max, y_min, z_max], 
        [x_max, y_max, z_max],
        [x_max, y_max, z_min]]


'Função que faz a separação da mesh em submeshs e escolhe a maior'
def separate(vertex, faces, d_max=2):
    new_faces = list()
    for face in faces:
        p1 = vertex[face[0]]
        p2 = vertex[face[1]]
        p3 = vertex[face[2]]
        if not (distance(p1, p2) > d_max or distance(p2, p3) > d_max or distance(p1,p3) > d_max):
            new_faces.append(face)

    mesh = form_mesh(np.array(vertex), np.array(new_faces))
    meshs = separate_mesh(mesh)
    max_v = 0
    for i in range(len(meshs)):
        if meshs[i].num_vertices > max_v:
            max_v = meshs[i].num_vertices
            mesh = meshs[i]

    pcloud_2d = cloud2D(mesh.vertices)
    face = Delaunay(pcloud_2d)
    face = [(p[0], p[1], p[2]) for p in face.simplices]
        
    return parseToList(mesh.vertices), face