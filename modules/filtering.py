import pcl
from aux.parser import parseToArray
from aux.files import log
from aux.calc import distance


'Remoção de outliers da nuvem de pontos'
def removeOutliers(point_cloud, min_dist=5, min_val=5):
    log("Removendo outliers da nuvem de pontos")

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
        condition_val =  point['value'] >= min_val
        condition_dist = distance((point['x'], point['y']), (0, 0)) > min_dist
        if condition_dist and condition_val:
            new_point_cloud.append(point)
    return new_point_cloud


'Remoção de ruído da nuvem de pontos'
def removeNoise(point_cloud):
    log("Removendo ruídos da nuvem de pontos")

    'Filtro de remoção de segmentos desnecessários'
    pc = pcl.PointCloud(parseToArray(point_cloud))
    seg = pc.make_segmenter_normals(searchRadius=10)
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(2)
    seg.set_normal_distance_weight(2)
    seg.set_distance_threshold(1)
    indices, model = seg.segment()
    pc = pc.extract(indices)

    'Filtro de remoção de ruídos'
    pc = pc.make_statistical_outlier_filter()
    pc.set_mean_k(100)
    pc.set_std_dev_mul_thresh(1.5)
    pc = pc.filter()
    pc = pc.to_array()
    
    return pc


'Suavização da nuvem de pontos'
def smoothing(point_cloud):
    log("Suavizando da nuvem de pontos")

    pc = pcl.PointCloud(point_cloud)
    pc = pc.make_moving_least_squares()
    pc.set_search_radius(5)
    pc.set_polynomial_fit(True)
    pc = pc.process()
    pc = pc.to_array()
    
    return pc