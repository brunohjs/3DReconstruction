import sys
import time

from modules.aux.io import plyToList, plyToCloud
from modules.aux.geometry import *
from modules.reconstruction import *

'Cálculo da parte superior '
def topSide(points):
    points = getPointMaxValAxis(points)
    if points[1][0] == points[2][0]:
        points.append([points[1][0], points[0][1], points[0][2]])
        area = areaTriangle([points[0], points[3], points[1]])
        #height = distance(points[3], points[2])
        height = getHeight(vet(points[3], points[2]), vet(points[3], points[1]))
    else:
        points.append([points[2][0], points[0][1], points[0][2]])
        points.append([points[2][0], points[1][1], points[1][2]])
        area = (distance(points[0], points[3]) + distance(points[1], points[4]))*distance(points[3], points[4])/2
        height = getHeight(vet(points[3], points[0]), vet(points[3], points[4]))
    volume = area*height/3
    return volume, points


'Cálculo da parte inferior de um prisma'
def bottomSide(points, height):
    if len(points) == 5:
        area = areaTriangle([points[2], points[3], points[4]])
    else:
        area = areaTriangle([points[1], points[2], points[3]])
    volume = area*height
    return volume


'Cálculo do volume de um prisma do sólido'
def volumePrism(p1, p2, p3, height):
    points = [p1, p2, p3]
    pyramid_volume, points = topSide(points)
    height = abs(height - points[3][0])
    prism_volume = bottomSide(points, height)
    return pyramid_volume + prism_volume


'Cálculo do volume total de um sólido'
def volume(plyfile, depth=None):
    if type(plyfile) == str:
        vertex, face = plyToList(plyfile)
    else:
        vertex, face = reconstructSurface(plyfile)
        depth = getMaxValAxis(plyfile)
        print(depth)
    total_volume = 0
    for i in range(len(face)):
        total_volume += volumePrism(vertex[face[i][0]], vertex[face[i][1]], vertex[face[i][2]], depth)
    return total_volume


'Relatório'
def volumeCompare(cloud1, cloud2, average_val):
    volume1 = volume(cloud1 + '/surface.ply', average_val)
    vertex, face = reconstructSurface(plyToCloud(cloud1 + '/surface.ply'))
    area1 = totalArea(vertex, face)

    volume2 = volume(cloud2 + '/surface.ply', average_val)
    vertex, face = reconstructSurface(plyToCloud(cloud2 + '/surface.ply'))
    area2 = totalArea(vertex, face) 
    
    print('_'*30)
    print('Resultado da comparação de volume:')
    print('_'*5)
    print(cloud1)
    print('volume: ', volume1)
    print('área: ', area1)
    print('_'*5)
    print(cloud2)
    print('volume: ', volume2)
    print('área: ', area2)
    print('_'*5)
    result = volume1 - volume2
    percent = abs(result)/volume1*100
    if result > 0:
        print('PERDA de %6.2f%% de volume.'%(percent))
    else:
        print('GANHO de %6.2f%% de volume.'%(percent))
    print('_'*30)
