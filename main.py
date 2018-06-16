import cv2
import numpy as np
import pylab as plb
import sys

'Classe que representa um bin do sonar MSIS'
class Bin:
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
        self.raw = self.convertRaw(list(line[9:-1]))

    'Função que faz um pré-processamento do vetor de bins'
    def convertRaw(self, raw):
        new_raw = list()
        for i in range(len(raw)):
            new_raw.append(float(self.raw[i]))
        return new_raw


'Função que pega os dados do dataset e passa para uma lista'
def getDataset(file, num_bins):
    dataset = list()
    f = open(file)
    for line in f.readlines()[1:num_bins+1]:
        dataset.append(Bin(line.split(',')))
    f.close()
    return dataset

'Mostra os bins em uma imagem (coordenadas cartesianas)'
def showImg(bins):
    img = list()
    for bin_line in bins:
        img.append(bin_line.raw)
    img = np.asarray(img)
    im = plb.imshow(img)
    #plb.colorbar(im, orientation='horizontal')
    plb.show()

'Função principal'
def main():
    bins = getDataset(sys.argv[1], 150)
    showImg(bins)


if __name__ == '__main__':
    main()