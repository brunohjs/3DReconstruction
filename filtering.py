import numpy as np
import pcl


'Remoção de outliers da nuvem de pontos'
def removeOutliers(point_cloud, min_val=5, min_dist=5):
    new_point_cloud = list()

    minimum = float('inf')
	maximum = 0
	for point in points:
		if point[param] < min_val:
			min_val = point[param]
		if point[param] > max_val:
			max_val = point[param]

    min_val = (((maximum - minimun)/100) * min_val) + minimun

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

    'Filtro de remoção de outliers'
    pc = pcl.PointCloud(np.array(points, dtype=np.float32))
    pc = pc.make_statistical_outlier_filter()
    pc.set_mean_k(100)
    pc.set_std_dev_mul_thresh(1.2)
    pc = pc.filter()

    'Filtro de suavização (MLS)'
    pc = pc.make_moving_least_squares()
    pc.set_search_radius(3)
    pc.set_polynomial_fit(0.5)
    pc = pc.process()
    pc = pc.to_list()

    points = list()
    for point in pc:
        points.append({
            'x': point[0],
            'y': point[1],
            'z': point[2]
        })
    
    return points