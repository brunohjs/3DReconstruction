from scipy.spatial import Delaunay
from shapely.geometry import Polygon, MultiPolygon
import itertools as it
import numpy as np


def distance(p1, p2, d2=False):
    if d2:
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
    else:
	    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)**0.5


def getNearPoint(point, points, near_size=1):
    near_points = list()
    for i in range(len(points)):
        d = distance(point, points[i], True)
        if len(near_points) < near_size:
            if len(near_points) == 0:
                near_points.append([i, points[i], d])
            else:
                for j in range(len(near_points)):
                    if d < near_points[j][2]:
                        near_points.insert(j, [i, points[i], d])
                        break
                    elif j == len(near_points)-1:
                        near_points.append([i, points[i], d])
        else: 
            for j in range(len(near_points)):
                if d < near_points[j][2]:
                    near_points.insert(j, [i, points[i], d])
                    near_points.pop()
                    break
    return near_points


points = [
    [1,1],
    [1,3],
    [2,3],
    [3,2],
    [4,1],
    [4,4],
    [4,5],
    [5,2]
]

points2 = [
    [0, 0],
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
    [1, 1],
    [2, 2]
]

print(points)
print(getNearPoint([5,2], points, 4))

hull = Delaunay(points2)
face = hull.simplices
for i in range(len(hull.points)):
    print(i, hull.points[i])

"""
for i in range(len(face)):
    p = Polygon([hull.points[face[i][0]], hull.points[face[i][1]], hull.points[face[i][2]]])
    if m.intersects(p) or m.is_empty:
        m = m.union(p)
    print(m)
m = m.convex_hull
print(m.is_simple)
m = Delaunay(list(m.exterior.coords)[:-1])
print(m.points)
print(m.simplices)
"""