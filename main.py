from convert import *
from Beam import Beam
import numpy as np
import pylab as plb
import sys


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
    elif type_ == 'higher_plot':
        for beam in beams:
            img.append(beam.bins.index(beam.higher))
            print(polar2Cartesian())
    
    #img = np.asarray([1,2,3,4])
    plb.plot(img, 'o')
    #im = plb.imshow(img)
    #plb.colorbar(im, orientation='horizontal')
    plb.show()

    #plt.plot([1, 2, 3, 4])
    #plt.ylabel('some numbers')
    #plt.show()

'Função principal'
def main():
    beams = getDataset(sys.argv[1], 150)
    showImg(beams, 'higher_plot')


if __name__ == '__main__':
    main()