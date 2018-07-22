import os.path
import os
import sys
import numpy as np
import pcl

'Função que printa logs no terminal'
def log(text):
    print('>', text)

'Função para salvar nuvem de pontos em arquivo nos formatos .ply e .pcd'
def saveFile(point_cloud, filename=None, ftype='.ply', original=False):
    if not os.path.exists("outputs/"):
        os.mkdir("outputs/")
    if filename:
        path = "outputs/" + filename
    else:
        splited_name = os.path.splitext(os.path.basename(sys.argv[1]))
        if original:
            path = "outputs/" + splited_name[0] + '_original' + ftype
            log("Salvando nuvem de pontos original em: "+path)
        else:
            path = "outputs/" + splited_name[0] + ftype
            log("Salvando nuvem de pontos em: "+path)

    if type(point_cloud) is np.ndarray:
        point_cloud = pcl.PointCloud(point_cloud)
    elif type(point_cloud) is list:
        point_cloud = pcl.PointCloud(parseToArray(point_cloud))
    pcl.save(point_cloud, path)


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