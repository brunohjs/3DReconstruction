import cv2
import numpy as np
import pylab as plb

file = open('data.txt')

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
        self.raw = list(line[9:-1])

        for i in range(len(self.raw)):
            self.raw[i] = float(self.raw[i])

img = list()
bins = list()


for line in file.readlines()[1:151]:
    bins.append(Bin(line.split(',')))
    print(line)

file.close()

for bin_line in bins:
    img.append(bin_line.raw)

img = np.asarray(img)

im = plb.imshow(img)
#plb.colorbar(im, orientation='horizontal')
plb.show()