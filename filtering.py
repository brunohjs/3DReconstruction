import numpy as np
import pcl


'Remoção de outliers da nuvem de pontos'
def removeOutliers(point_cloud, min_val=5, min_dist=5):
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
        condition_dist = point['dist'] > min_dist
        condition_val =  point['value'] >= min_val
        if condition_dist and condition_val:
            new_point_cloud.append(point)
    return new_point_cloud


'Remoção de ruído e suavização da nuvem de pontos'
def removeNoise(point_cloud):
    points = list()
    for point in point_cloud:
        points.append([
            point['x'],
            point['y'],
            point['z']
        ])

    'Filtro de suavização (MLS)'
    pc = pcl.PointCloud(np.array(points, dtype=np.float32))
    pc = pc.make_moving_least_squares()
    pc.set_search_radius(3)
    pc.set_polynomial_fit(0.5)
    pc = pc.process()

    'Filtro de remoção de segmentos desnecessários'
    seg = pc.make_segmenter_normals(searchRadius=10)
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SACMODEL_NORMAL_PLANE)
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
    pc = pc.to_list()

    points = list()
    for point in pc:
        points.append({
            'x': point[0],
            'y': point[1],
            'z': point[2]
        })
    
    return points