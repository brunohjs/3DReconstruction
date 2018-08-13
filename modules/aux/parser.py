import numpy as np
import math
import pcl


'Conversão de coordenadas cartesianas para polares'
def cartesian2Polar(x, y):
    rho = math.sqrt(x**2 + y**2)
    phi = math.atan2(y, x)
    return (rho, phi)


'Conversão de coordenadas polares para cartesianas'
def polar2Cartesian(dist, angle):
    x = dist * math.cos(angle)
    y = dist * math.sin(angle)
    return (x, y)


'Conversão de ângulos em quaternion para Euler'
def quaternion2Euler(x, y, z, w):
	t0 = 2 * (w * x + y * z)
	t1 = 1 - 2 * (x * x + y**2)
	X = math.atan2(t0, t1)
	t2 = 2 * (w * y - z * x)
	t2 = +1 if t2 > +1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = math.asin(t2)
	t3 = +2 * (w * z + x * y)
	t4 = +1 - 2 * (y**2 + z * z)
	Z = math.atan2(t3, t4)
	return X, Y, Z


'Converte o dataset para uma nuvem de pontos'
def parseToArray(dataset):
    points = list()
    for point in dataset:
        points.append([
            point['x'],
            point['y'],
            point['z']
        ])
    return np.array(points, dtype=np.float32)


'Função para converter uma lista ou array em nuvem de pontos'
def parseToPointCloud(var):
    if type(var) is np.ndarray:
        return pcl.PointCloud(var)
    elif type(var) is list:
        if type(var[0]) is dict:
            return pcl.PointCloud(parseToArray(var))
        else:
            return pcl.PointCloud(np.array(var, dtype=np.float32))
    else:
        return var


'Função para converter os pontos para uma lista'
def parserToList(array):
    if type(array) is np.ndarray:
        new_list = list()
        for point in array:
            new_list.append(list(point))
        return new_list