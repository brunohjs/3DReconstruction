import sys
import time

from modules.aux.geometry import *
from modules.aux.io import *
from modules.filtering import *
from modules.pre_processing import *
from modules.reconstruction import *


def pyramid(points):
    points = getPointMaxValAxis(points)
    if points[1][0] == points[2][0]:
        points.append([points[1][0], points[0][1], points[0][2]])
        area = areaTriangle([points[0], points[3], points[2]])
        height = distance(points[3], points[1])
    else:
        points.append([points[2][0], points[0][1], points[0][2]])
        points.append([points[2][0], points[1][1], points[1][2]])
        area = (distance(points[0], points[3]) + distance(points[1], points[4]))*distance(points[3], points[4])/2
        height = distance(midPoint(points[3], points[4]), points[2])
    volume = area*height/3
    print(points, volume, area, height)
    return volume, points


def prism(points, height):
    if len(points) == 5:
        area = areaTriangle([points[2], points[3], points[4]])
    else:
        area = areaTriangle([points[1], points[2], points[3]])
    volume = area*height
    return volume


def volume(p1, p2, p3, height):
    points = [p1, p2, p3]
    pyramid_volume, points = pyramid(points)
    height = height - points[3][0]
    prism_volume = prism(points, height)
    #print(prism_volume, pyramid_volume)
    return pyramid_volume + prism_volume

def totalVol(vertex, face):
    max_val = getMaxValAxis(vertex)
    total_volume = 0
    for i in range(len(face)):
        total_volume += volume(vertex[face[i][0]], vertex[face[i][1]], vertex[face[i][2]], 28)
        #print(face[i] , volume(vertex[face[i][0]], vertex[face[i][1]], vertex[face[i][2]], 28))
    return total_volume
    


vertex, face = plyToList(sys.argv[1])
print(totalVol(vertex, face))
