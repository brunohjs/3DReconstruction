from calc import polar2Cartesian

import os.path
import os
import sys
import plyfile

from mpl_toolkits.mplot3d import Axes3D
import pylab as plb
import numpy as np



global RANGE
RANGE = 50

'Pegar o dataset do arquivo texto'
def getDataset(file):
    dataset = list()
    f = open(file)
    for line in f.readlines()[1:]:
        aux = line.rstrip().split(',')
        beam = {
            'id': int(aux[0]),
            'angle': float(aux[1]),
            'x': float(aux[2]),
            'y': float(aux[3]),
            'z': float(aux[4]),
            'ox': float(aux[5]),
            'oy': float(aux[6]),
            'oz': float(aux[7]),
            'ow': float(aux[8]),
            'raw': aux[9:-1]
        }
        for i in range(len(beam['raw'])):
            beam['raw'][i] = float(beam['raw'][i])
        dataset.append(beam)
    return dataset

'Separar o dataset em imagens'
def splitDataset(dataset):
    clockwise = False
    data = list()
    image = list()
    previous = dataset[0]['angle']
    for line in dataset[1:]:
        cond_left = line['angle'] < previous and not clockwise
        cond_right = line['angle'] > previous and clockwise
        previous = line['angle']

        if cond_left or cond_right:
            clockwise = not clockwise
            data.append(image)
            image = list()
        image.append(line)
    return data

'Ordenar os beams nas imagens'
def ordenizeDataset(dataset):
    for i in range(len(dataset)):
        if i%2 == 1:
            dataset[i] = dataset[i][::-1]
    return dataset

'Função que coleta o maior valor e a posição de um bin em um beam'
def getHigherBin(dataset):
    for image in dataset:
        for beam in image:
            higher = 0
            higher_index = -1
            for bin_ in beam['raw']:
                if bin_ > higher:
                    higher = bin_
                    higher_index = beam['raw'].index(bin_)
            beam['higher'] = {
                'value': higher, 
                'dist' : (higher_index+1)*len(beam['raw'])/RANGE,
                'index': higher_index
            }
        if len(image) > 179:
            image.remove(image[-1])
    return dataset

'Passa os dados para vetores que serão plotados em 3D'
def transpose(dataset, outliers=2):
    axis_x = list()
    axis_y = list()
    axis_z = list()
    axis_c = list()
    for image in dataset:
        axis_x.append(list())
        axis_y.append(list())
        axis_z.append(list())
        axis_c.append(list())
        for beam in image:
            if beam['higher']['dist'] <= 1:
                if outliers is 1:
                    x, y = polar2Cartesian(RANGE, beam['angle'])
                    z = beam['z']
                elif outliers is 2:
                    x, y = -1, -1
                    z = -92
            else:
                x, y = polar2Cartesian(beam['higher']['dist'], beam['angle'])
                z = beam['z']        
            axis_x[-1].append(x)
            axis_y[-1].append(y)
            axis_z[-1].append(z)
            axis_c[-1].append(beam['higher']['value'])
    
    #plot3D(axis_x, axis_y, axis_z, axis_c)
    return axis_x, axis_y, axis_z

'Converter a nuvem de pontos em um arquivo .ply'
def saveFile(x,y,z):
    points = list()
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] != -1 and y[i][j] != -1:
                vert = (x[i][j], y[i][j], z[i][j])
                points.append(vert)
    points = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    point_cloud = plyfile.PlyElement.describe(points, 'vertex')
    
    if not os.path.exists("point_clouds/"):
        os.mkdir("point_clouds/")
    namefile = "point_clouds/"+os.path.splitext(os.path.basename(sys.argv[1]))[0]
    plyfile.PlyData([point_cloud], text=True).write(namefile+'.ply')


'Plota o gráfico em 3D'
def plot3D(x, y, z, c):
    fig = plb.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(np.array(x), np.array(y), np.array(z),c=np.array(c), s=20, linewidths=0)
    #ax.set_xlim3d(-60, 60)
    #ax.set_ylim3d(-60, 60)
    #ax.set_zlim3d(-96, -50)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_zlabel("Eixo Z")
    plb.show()


'Função principal'
def main():
    dataset = getDataset(sys.argv[1])
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset)
    x,y,z = transpose(dataset)
    saveFile(x, y, z)


if __name__ == '__main__':
    main()
    