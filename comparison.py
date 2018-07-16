from modules.files import saveFile
import pcl

def comparison(cloud1, cloud2, resolution=4):
    octree = cloud1.make_octreeChangeDetector(resolution)
    octree.add_points_from_input_cloud()
    octree.switchBuffers()

    octree.set_input_cloud(cloud2)
    octree.add_points_from_input_cloud()

    index_vector_result = octree.get_PointIndicesFromNewVoxels()
    cloud_result = cloud2.extract(index_vector_result)

    cloud_result = cloud_result.to_list()
    points = list()
    for point in cloud_result:
        points.append({
            'x': point[0],
            'y': point[1],
            'z': point[2]
        })

    return points