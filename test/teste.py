from scipy.spatial import Delaunay
from pyhull.convex_hull import *
from modules.calc import combination
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
    [0, 0, 0],
    [0, 2, 0],
    [2, 0, 0],
    [2, 2, 0],
    [0, 0, 1],
]

hull = Delaunay(points2)
print(hull.points)
print(hull.simplices)
print(combination(hull.simplices[0]))
