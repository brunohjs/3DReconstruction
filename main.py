import sys
import time
from modules.files import saveFile, log

from pre_processing import *
from filtering import *
from reconstruction import *
from comparison import *



def main():
    t0 = time.time()

    'Pré-processamento'
    dataset = getDataset(sys.argv[1])
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset)
    pcloud_original = generatePointCloud(dataset)
    
    saveFile(pcloud_original, type_='original')

    'Filtragem'
    pcloud = removeOutliers(pcloud_original)
    pcloud = removeNoise(pcloud)
    pcloud = smoothing(pcloud)
    
    'Reconstrução'
    #pcloud = reconstruct(pcloud)

    'Comparação'
    pcloud_result = comparison(pcloud, pcloud_original)

    'Salvar em arquivo'
    saveFile(pcloud)
    saveFile(pcloud_result, type_='result')

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)
    

if __name__ == '__main__':
    main()