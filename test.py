from modules.reconstruction import *
from modules.aux.volume import *
from modules.pre_processing import *


def getHigherBins(dataset, range_bin=60, nbeams=10):
    new_dataset = list()
    for image in dataset:
        for beam in image:
            highers = list()
            for i, bin_ in enumerate(beam['raw']):
                if len(highers) < 10:
                    highers.append((bin_, i))
                else:
                    for j in range(len(highers)):
                        if bin_ > highers[j][0]:
                            highers[j] = (bin_, i)
                            break
            for i in range(len(highers)):
                aux = dict()
                aux['value'] = highers[i][0]
                aux['dist'] = (highers[i][1]+1)/len(beam['raw'])*range_bin
                aux['index'] = highers[i][1]
                new_dataset.append(aux)
            
    return new_dataset

dataset = getDataset('inputs/perto.txt')
dataset = splitDataset(dataset, 200)
dataset = getHigherBins(dataset)
print(dataset)