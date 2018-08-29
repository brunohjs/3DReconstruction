import itertools as it
from shapely.geometry import Polygon
from modules.aux.parser import parserToList


'Distância euclidiana entre dois pontos'
def distance(p1, p2, d2=False):
    if d2:
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
    else:
	    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)**0.5


'Fórmula para calcular área de qualquer triângulo (fórmula de Heron)'
def areaTriangle(points):
    a = distance(points[0], points[1])
    b = distance(points[1], points[2])
    c = distance(points[2], points[0])
    p = (a+b+c)/2
    return (p*(p-a)*(p-b)*(p-c))**0.5


'Função para validar faces'
def validadeFace(shape):
    faces = list(it.permutations(shape, 4))
    for face in faces:
        polygon = LinearRing([face[0][0], face[1][0], face[2][0], face[3][0]])
        if polygon.is_valid:
            return [face[0][1], face[1][1], face[2][1], face[3][1]]


'Função que retorna a área total da superfície'
def totalArea(vertex, faces):
    total_area = 0
    for face in faces:
        total_area += areaTriangle([vertex[face[1]], vertex[face[2]], vertex[face[3]]])
    return total_area


'Retorna o menor valor de um eixo na nuvem de pontos'
def getMaxValAxis(pcloud, axis='x'):
    if axis == 'x':
        axis = 0
    elif axis == 'y':
        axis = 1
    elif axis == 'z':
        axis = 2

    max_val = float('-inf')
    for point in pcloud:
        if point[axis] > max_val:
            max_val = point[axis]
    return max_val