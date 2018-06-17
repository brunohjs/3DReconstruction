from calc import *
from Beam import Beam
import numpy as np
import pylab as plb
import sys

'Função que pega os dados do dataset e passa para uma lista'
def getDataset(file, num_bins):
    dataset = list()
    f = open(file)
    for line in f.readlines()[1:num_bins+1]:
        dataset.append(Beam(line.split(',')))
    f.close()
    return dataset[::-1]

'Mostra os beams em uma imagem (coordenadas cartesianas)'
def showImg(beams, type_='normal'):
    img = list()
    img_x = list()
    img_y = list()
    
    if type_ == 'normal':
        for beam in beams:
            img.append(beam.bins)
        img = np.asarray(img)
        im = plb.imshow(img)
    elif type_ == 'higher':
        for beam in beams:
            line_img = list()
            for bin_ in beam.bins:
                if bin_ == beam.higher:
                    line_img.append(1)
                elif bin_ > 0:
                    line_img.append(0.5)
                else:
                    line_img.append(0)
            img.append(line_img)
        img = np.asarray(img)
        im = plb.imshow(img, cmap='binary')
    elif type_ == 'higher_plot':
        for beam in beams:
            img_x.append(beam.higher_x)
            img_y.append(beam.higher_y)
        plb.plot(img_x, img_y, '.')
        #plb.axis([5, 30, 30, -30])
    
    #plb.colorbar(im, orientation='horizontal')
    plb.show()

'Função principal'
def main():
    beams = getDataset(sys.argv[1], 150)
    showImg(beams, 'normal')

if __name__ == '__main__':
    main()