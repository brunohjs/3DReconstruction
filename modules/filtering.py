import pcl
from math import radians, degrees

from modules.aux.parser import parseToPointCloud
from modules.aux.io import log
from modules.aux.geometry import distance



'Filtro que diminui o ângulo horizontal da coleta de dados do sensor'
def removeExtAnglePoints(point_cloud, angle):
    log(" - Removendo pontos fora do ângulo de abertura horizontal")

    new_point_cloud = list()
    angle = radians(angle)
    for point in point_cloud:
        if abs(point['angle']) <= angle/2:
            new_point_cloud.append(point)
    return new_point_cloud


'Filtro que remove pontos próximos ao robô'
def removeMinDistPoints(point_cloud, min_dist):
    log(" - Removendo pontos próximos ao sensor.")

    new_point_cloud = list()
    for point in point_cloud:
        if point['dist'] > min_dist:
            new_point_cloud.append(point)
    return new_point_cloud


'Filtro que remove pontos próximos ao robô'
def removeMaxDistPoints(point_cloud, max_dist):
    log(" - Removendo pontos próximos ao sensor.")

    new_point_cloud = list()
    for point in point_cloud:
        if point['dist'] < max_dist:
            new_point_cloud.append(point)
    return new_point_cloud


'Filtro que remove pontos com baixo valor de intensidade'
def removeMinValPoints(point_cloud, min_val):
    log(" - Removendo pontos com baixo valor de intensidade")

    new_point_cloud = list()
    minimum = float('inf')
    maximum = 0
    for point in point_cloud:
        if point['value'] < minimum:
            minimum = point['value']
        if point['value'] > maximum:
            maximum = point['value']
    
    min_val = (((maximum - minimum)/100) * min_val) + minimum

    for point in point_cloud:
        if point['value'] >= min_val:
            new_point_cloud.append(point)
    return new_point_cloud


'Remoção de outliers da nuvem de pontos'
def removeOutliers(point_cloud, min_val=1.5, min_dist=15, max_dist=20, angle=120):
    log("Removendo outliers da nuvem de pontos:")
    
    new_point_cloud = removeExtAnglePoints(point_cloud, angle)
    new_point_cloud = removeMinDistPoints(new_point_cloud, min_dist)
    new_point_cloud = removeMaxDistPoints(new_point_cloud, max_dist)
    new_point_cloud = removeMinValPoints(new_point_cloud, min_val)

    return new_point_cloud


'Remoção de ruído da nuvem de pontos'
def staticalOutlierFilter(point_cloud):
    log("Removendo ruídos da nuvem de pontos")

    pc = parseToPointCloud(point_cloud)

    pc = pc.make_statistical_outlier_filter()
    pc.set_mean_k(15)
    pc.set_std_dev_mul_thresh(1)
    pc = pc.filter()
    pc = pc.to_array()

    return pc


'Suavização da nuvem de pontos'
def smoothingFilter(point_cloud):
    log("Suavizando da nuvem de pontos")

    pc = parseToPointCloud(point_cloud)
    pc = pc.make_moving_least_squares()
    pc.set_search_radius(5)
    pc.set_polynomial_fit(True)
    pc = pc.process()
    pc = pc.to_array()
    
    return pc


'Função para remover pontos próximos'
def downsamplerFilter(point_cloud, space=1):
    log("Removendo pontos próximos na nuvem")

    pc = parseToPointCloud(point_cloud)
    pc = pc.make_voxel_grid_filter()
    pc.set_leaf_size(space, space, space)
    pc = pc.filter()
    pc = pc.to_array()
    
    return pc
