import itertools as it
from shapely.geometry import Polygon


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
        total_area += areaTriangle([vertex[face[0]], vertex[face[1]], vertex[face[2]]])
    return total_area


'Módulo de um vetor'
def mod(v):
    return (v[0]**2 + v[1]**2 + v[2]**2)**0.5


'Cria um vetor a partir dos pontos p1 e p2'
def vet(p1, p2):
    return [p2[i] - p1[i] for i in range(3)]


'Função que retorna a altura distância do vetor v1 sobre v2'
def getHeight(v1, v2):
    a = dot(v1, unit(v2))
    v = [a*unit(v2)[i] for i in range(3)]
    a = [v1[i] - v[i] for i in range(3)]
    return mod(a)


'Produto escalar entre os vetores'
def dot(v1, v2):
    return sum([v1[i]*v2[i] for i in range(3)])


'Vetor unitário'
def unit(v):
    u = mod(v)
    return [v[i]/u for i in range(3)]


'Ponto médio entre dois pontos'
def midPoint(p1, p2):
    p = list()
    for i in range(3):
        p.append((p1[i] + p2[i])/2)
    return p


'Retorna o maior valor de um eixo na nuvem de pontos'
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


'Retorna o maior valor de um eixo na nuvem de pontos'
def getMinValAxis(pcloud, axis='x'):
    if axis == 'x':
        axis = 0
    elif axis == 'y':
        axis = 1
    elif axis == 'z':
        axis = 2

    min_val = float('inf')
    for point in pcloud:
        if point[axis] < min_val:
            min_val = point[axis]
    return min_val


'Retorna o valor do ponto mais distante em um determinado eixo entre duas nuvem de pontos'
def averageDepth(pcloud1, pcloud2, dist=5):
    depth1 = getMaxValAxis(pcloud1)
    depth2 = getMaxValAxis(pcloud2)
    return max(depth1, depth2) + dist


'Organiza os pontos em ordem decrescente de proximidade do plano base (os mais próximos ao plano base, serão os últimos)'
def getPointMaxValAxis(points, axis='x'):
    if axis == 'x':
        axis = 0
    elif axis == 'y':
        axis = 1
    elif axis == 'z':
        axis = 2

    for i in range(len(points)-1):
        aux = 0
        for j in range(i+1, len(points)):
            if points[i][axis] > points[j][axis]:
                aux = points[i]
                points[i] = points[j]
                points[j] = aux
    return points


'Função para reposicionar uma nuvem de pontos'
def translateClouds(cloud1, cloud2, axis='x'):
    move = [0, 0, 0]
    if axis == 'x':
        axis = 0
    elif axis == 'y':
        axis = 1
    elif axis == 'z':
        axis = 2
    
    min_val1 = getMinValAxis(cloud1, axis)
    min_val2 = getMinValAxis(cloud2, axis)
    move[axis] = abs(min_val2 - min_val1)
    if min_val1 < min_val2:
        for i in range(len(cloud1)):
            for j in range(len(cloud1[i])):
                cloud1[i][j] = cloud1[i][j] + move[j]
    elif min_val2 < min_val1:
        for i in range(len(cloud2)):
            for j in range(len(cloud2[i])):
                cloud2[i][j] = cloud2[i][j] + move[j]
    return cloud1, cloud2