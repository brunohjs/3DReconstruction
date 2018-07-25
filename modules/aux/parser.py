import numpy as np
import pcl

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