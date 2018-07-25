from modules.parser import parseToPointCloud

def comparison(cloud1, cloud2, resolution=4):
    cloud1 = parseToPointCloud(cloud1)
    cloud2 = parseToPointCloud(cloud2)

    octree = cloud1.make_octreeChangeDetector(resolution)
    octree.define_bounding_box()
    octree.add_points_from_input_cloud()
    octree.switchBuffers()

    octree.set_input_cloud(cloud2)
    octree.add_points_from_input_cloud()

    index_vector_result = octree.get_PointIndicesFromNewVoxels()
    cloud_result = cloud2.extract(index_vector_result)

    return cloud_result