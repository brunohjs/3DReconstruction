import sys
import time
from pre_processing import *
from filtering import *
from comparison import *
from modules.files import saveFile, log


def main():
    t0 = time.time()

    'Pré-processamento'
    dataset = getDataset(sys.argv[1])
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset)
    point_cloud = generatePointCloud(dataset)
    
    saveFile(point_cloud, original=True)

    'Filtragem'
    point_cloud = removeOutliers(point_cloud)
    point_cloud = removeNoise(point_cloud)
    point_cloud = smoothing(point_cloud)
    
    'Reconstrução'

    'Comparação'
    #point_cloud = comparison()

    'Salvar em arquivo'
    saveFile(point_cloud)

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)
    

if __name__ == '__main__':
    main()