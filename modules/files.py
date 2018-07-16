import plyfile
import os.path
import os
import sys
import numpy as np

'Converter a nuvem de pontos em um arquivo .ply'
def saveFile(dataset, filename=None):
    points = list()
    for point in dataset:
        vert = (point['x'], point['y'], point['z'])
        points.append(vert)
    points = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    point_cloud = plyfile.PlyElement.describe(points, 'vertex')
    
    if not os.path.exists("outputs/"):
        os.mkdir("outputs/")
    if filename:
        namefile = "outputs/"+filename
    else:
        namefile = "outputs/"+os.path.splitext(os.path.basename(sys.argv[1]))[0]+'.ply'
    plyfile.PlyData([point_cloud], text=True).write(namefile)