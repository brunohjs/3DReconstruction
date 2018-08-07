import itertools as it
from shapely.geometry import Polygon

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
		total_area += Polygon([vertex[face[1]], vertex[face[2]], vertex[face[3]]]).area
	return total_area