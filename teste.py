from modules.pre_processing import *
from modules.filtering import *
from modules.aux.global_vars import *
from modules.aux.parser import *
from sys import argv


def getPoints(array):
    f = open('teste.txt', 'w')
    for p in array:
        line = [str(p['angle']), str(p['z']), str(p['dist']), str(round(p['x'],4)), str(round(p['y'],4)), str(p['z'])]
        line = ' '.join(line)
        f.write(line+'\n')
    f.close()

def getPoints2(array):
    f = open('teste.txt', 'w')
    for p in array:
        dist, angle = cartesian2Polar(p[0], p[1])
        dist, angle = round(dist, 4), round(angle, 4)
        line = [str(angle), str(p[2]), str(dist), str(round(p[0],4)), str(round(p[1],4)), str(p[2])]
        line = ' '.join(line)
        f.write(line+'\n')
    f.close()


dataset = getDataset(argv[1])
dataset = splitDataset(dataset)
dataset = ordenizeDataset(dataset)
dataset = getHigherBin(dataset, RANGE)
pcloud_original = generatePointCloud(dataset)

pcloud = removeOutliers(pcloud_original)
pcloud = staticalOutlierFilter(pcloud)
pcloud = smoothingFilter(pcloud)
pcloud = downsamplerFilter(pcloud, space=1)

getPoints2(pcloud)