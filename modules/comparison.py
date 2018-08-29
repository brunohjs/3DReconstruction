from modules.aux.parser import parseToPointCloud
from modules.aux.geometry import getMaxValAxis
from modules.aux.io import saveFile, log

'Comparação entre duas nuvem de pontos e retorna a nuvem de pontos resultante'
def comparison(cloud1, cloud2, resolution=2):
    log('Comparando modelos')

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


'Retorna o valor do ponto mais distante em um determinado eixo entre duas nuvem de pontos'
def averageDepth(pcloud1, pcloud2, dist=5):
    depth1 = getMaxValAxis(pcloud1)
    depth2 = getMaxValAxis(pcloud2)
    return max(depth1, depth2) + dist