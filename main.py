
import numpy as np
import pylab as plb
import sys
from math import asin,atan2

'Classe que representa um bin do sonar MSIS'
class Beam:
    def __init__(self, line):
        self.frame = int(line[0])
        self.angle_head = float(line[1])
        
        self.position_x = float(line[2])
        self.position_y = float(line[3])
        self.position_z = float(line[4])

        self.orientation_x = float(line[5])
        self.orientation_y = float(line[6])
        self.orientation_z = float(line[7])
        self.orientation_w = float(line[8])

        (self.angular_x, 
        self.angular_y, 
        self.angular_z) = quaternion2EulerAngle(
            self.orientation_x, 
            self.orientation_y,
            self.orientation_z,
            self.orientation_w)
        
        self.bins = convertRaw(list(line[9:-1]))
        self.higher = max(self.bins)
         


'Função que faz um pré-processamento do vetor de beams'
def convertRaw(raw):
    bins = list()
    for i in range(len(raw)):
        bins.append(float(raw[i]))
    return bins

'Função que pega os dados do dataset e passa para uma lista'
def getDataset(file, num_bins):
    dataset = list()
    f = open(file)
    for line in f.readlines()[1:num_bins+1]:
        dataset.append(Beam(line.split(',')))
    f.close()
    return dataset

'Mostra os beams em uma imagem (coordenadas cartesianas)'
def showImg(beams, type_='normal'):
    img = list()
    
    if type_ == 'normal':
        for beam in beams:
            img.append(beam.bins)
    elif type_ == 'higher':
        for beam in beams:
            line_img = list()
            for bin_ in beam.bins:
                if bin_ == beam.higher:
                    line_img.append(beam.higher)
                else:
                    line_img.append(0)
            img.append(line_img)
    
    img = np.asarray(img)
    im = plb.imshow(img)
    #plb.colorbar(im, orientation='horizontal')
    plb.show()

'Função que converte os ângulos de quaternion para Euler'
def quaternion2EulerAngle(x, y, z, w):
	t0 = 2 * (w * x + y * z)
	t1 = 1 - 2 * (x * x + y**2)
	X = atan2(t0, t1)
	t2 = 2 * (w * y - z * x)
	t2 = +1 if t2 > +1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = asin(t2)
	t3 = +2 * (w * z + x * y)
	t4 = +1 - 2 * (y**2 + z * z)
	Z = atan2(t3, t4)
	return X, Y, Z

'Função principal'
def main():
    beams = getDataset(sys.argv[1], 150)
    showImg(beams, 'higher')


if __name__ == '__main__':
    main()