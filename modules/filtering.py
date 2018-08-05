import pcl
from math import degrees

from modules.aux.parser import parseToPointCloud
from modules.aux.files import log
from modules.aux.calc import distance



'Filtro que diminui o ângulo horizontal da coleta de dados do sensor'
def removeExtAnglePoints(point_cloud, angle=120):
    log(" - Removendo pontos fora do ângulo de abertura horizontal")

    new_point_cloud = list()
    for point in point_cloud:
        if degrees(abs(point['angle'])) <= angle:
            new_point_cloud.append(point)
    return new_point_cloud


'Filtro que remove pontos próximos ao robô'
def removeMinDistPoints(point_cloud, min_dist=5):
    log(" - Removendo pontos próximos desnecessários")

    new_point_cloud = list()
    for point in point_cloud:
        if distance((point['x'], point['y'], point['z']), (0, 0, 0)) > min_dist:
            new_point_cloud.append(point)
    return new_point_cloud


'Filtro que remove pontos com baixo valor de intensidade'
def removeMinValPoints(point_cloud, min_val=5):
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
def removeOutliers(point_cloud, min_dist=5, min_val=5, angle=120):
    log("Removendo outliers da nuvem de pontos:")
    
    new_point_cloud = removeExtAnglePoints(point_cloud, 120)
    new_point_cloud = removeMinDistPoints(new_point_cloud, 5)
    new_point_cloud = removeMinValPoints(new_point_cloud, 5)
    
    return new_point_cloud


'Remoção de ruído da nuvem de pontos'
def staticalOutlierFilter(point_cloud):
    log("Removendo ruídos da nuvem de pontos")

    pc = parseToPointCloud(point_cloud)

    pc = pc.make_statistical_outlier_filter()
    pc.set_mean_k(500)
    pc.set_std_dev_mul_thresh(2)
    pc = pc.filter()
    pc = pc.to_array()

    return pc


'Filtro de remoção de segmentos desnecessários'
def segmentationFilter(point_cloud):
    log("Segmentação da nuvem de pontos")

    pc = parseToPointCloud(point_cloud)
    seg = pc.make_segmenter()
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SAC_RANSAC)
    seg.set_method_type(1)
    seg.set_distance_threshold(10)
    indices, model = seg.segment()
    pc = pc.extract(indices)
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
def disperseFilter(point_cloud, space=1):
    log("Removendo pontos próximos na nuvem")

    pc = parseToPointCloud(point_cloud)
    pc = pc.make_voxel_grid_filter()
    pc.set_leaf_size(space, space, space)
    pc = pc.filter()
    pc = pc.to_array()
    
    return pc


def radialFilter(point_cloud, radius=1):
    new_point_cloud = list()
    list_index_to_discart = list()
    for i in range(len(point_cloud)-1):
        for j in range(i+1, len(point_cloud)):
            d = distance(point_cloud[i], point_cloud[j])
            if d <= radius:
                list_index_to_discart.append(i)
                break
    for i in range(len(point_cloud)):
        if i in list_index_to_discart:
            continue
        else:
            new_point_cloud.append(point_cloud[i])
    return new_point_cloud
