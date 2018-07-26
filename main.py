import sys
import time
from modules.aux.files import saveFile, log

from modules.pre_processing import *
from modules.filtering import *
from modules.reconstruction import *
from modules.comparison import *



def main():
    t0 = time.time()

    'Pré-processamento'
    dataset = getDataset(sys.argv[1])
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset)
    pcloud_original = generatePointCloud(dataset)
    
    saveFile(pcloud_original, sufix='original')

    'Filtragem'
    pcloud = removeOutliers(pcloud_original)
    saveFile(pcloud, sufix='filt1')
    pcloud = removeNoise(pcloud)
    saveFile(pcloud, sufix='filt2')
    pcloud = smoothing(pcloud)
    
    'Reconstrução'
    #pcloud = reconstruct(pcloud)

    'Comparação'
    pcloud_result = comparison(pcloud, pcloud_original)

    'Salvar em arquivo'
    saveFile(pcloud)
    saveFile(pcloud_result, sufix='result')

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)
    

if __name__ == '__main__':
    main()