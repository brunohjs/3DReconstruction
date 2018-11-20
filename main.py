import sys
import time
from glob import glob

from modules.aux.io import *
from modules.aux.global_vars import *
from modules.aux.volume import *

from modules.pre_processing import *
from modules.filtering import *
from modules.reconstruction import *
from modules.comparison import *


def compare(c1_path, c2_path, translate=False):
    t0 = time.time()

    removeOldFiles([c1_path, c2_path], True)

    'Carregar arquivos das nuvens de pontos'
    cloud1 = plyToCloud(c1_path+'/surface_cloud.ply')
    cloud2 = plyToCloud(c2_path+'/surface_cloud.ply')

    'Transformar as nuvens em lista'
    cloud1 = parseToList(cloud1)
    cloud2 = parseToList(cloud2)
    if translate:
        cloud1, cloud2 = translateClouds(cloud1, cloud2)

    'Cálculo de volume'
    volumeCompare(cloud1, cloud2, c1_path, c2_path)

    'Comparar'
    pcloud_result = comparison(cloud1, cloud2)
    pcloud_result = staticalOutlierFilter(pcloud_result)

    'Reconstrução'
    back_points = similarBackPoints(cloud1, cloud2)
    cloud1 = cloud1 + back_points
    cloud2 = cloud2 + back_points
    
    pcloud, face = reconstructVolume(cloud1)
    saveFile(cloud1, [c1_path, c2_path], sufix=getNamePath(c1_path), comparison=True)
    saveFile(pcloud, [c1_path, c2_path], face=face, sufix=getNamePath(c1_path)+'_volume', comparison=True)
    
    pcloud, face = reconstructVolume(cloud2)
    saveFile(cloud2, [c1_path, c2_path], sufix=getNamePath(c2_path), comparison=True)
    saveFile(pcloud, [c1_path, c2_path], face=face, sufix=getNamePath(c2_path)+'_volume', comparison=True)

    #pcloud, face = reconstructVolume(pcloud_result, depth)
    #saveFile(pcloud, [c1_path, c2_path], face=face, sufix='surface', comparison=True)
    #saveFile(pcloud_result, [c1_path, c2_path], comparison=True)

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)


def experiment(args, RANGE=60):
    t0 = time.time()

    removeOldFiles(args)

    'Pré-processamento'
    dataset = getDataset(args)
    dataset = splitDataset(dataset, 200)
    dataset2 = getHigherBin(dataset, RANGE, 200)
    
    #pcloud_original = generatePointCloud(dataset2)
    #saveFile(pcloud_original, args, sufix='original')

    dataset = getHigherBins(dataset, RANGE, 1)
    pcloud_original = generatePointCloud(dataset)
    saveFile(pcloud_original, args, sufix='original')

    'Filtragem'
    pcloud = removeOutliers(pcloud_original, 5, 15, 40, 70)
    #saveFile(pcloud, args, sufix='filt1')
    pcloud = staticalOutlierFilter(pcloud)
    #saveFile(pcloud, args, sufix='filt2')
    pcloud = smoothingFilter(pcloud)
    #saveFile(pcloud, args, sufix='filt3')
    pcloud = downsamplerFilter(pcloud, space=1)
    #saveFile(pcloud, args, sufix='filt4')

    'Reconstrução'
    pcloud, face = reconstructSurface(pcloud)
    print('surface', len(pcloud))
    log(' - Volume total: '+str(volume(pcloud)))
    saveFile(pcloud, args, sufix='surface_cloud')
    saveFile(pcloud, args, face=face, sufix='surface')
    pcloud, face = reconstructVolume(pcloud)
    saveFile(pcloud, args, sufix='volume_cloud')
    saveFile(pcloud, args, face=face, sufix='volume')

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)


def main(args):
    t0 = time.time()

    removeOldFiles(args)

    'Pré-processamento'
    dataset = getDataset(args)
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset, RANGE)
    pcloud_original = generatePointCloud(dataset)
    
    saveFile(pcloud_original, args, sufix='original')
    
    'Filtragem'
    pcloud = removeOutliers(pcloud_original)
    #saveFile(pcloud, args, sufix='filt1')
    pcloud = staticalOutlierFilter(pcloud)
    #saveFile(pcloud, args, sufix='filt2')
    pcloud = smoothingFilter(pcloud)
    #saveFile(pcloud, args, sufix='filt3')
    pcloud = downsamplerFilter(pcloud, space=1)

    'Reconstrução'
    
    pcloud, face = reconstructSurface(pcloud)
    saveFile(pcloud, args, sufix='surface_cloud')
    saveFile(pcloud, args, face=face, sufix='surface')
    log(' - Volume total: '+str(volume(pcloud)))
    pcloud, face = reconstructVolume(pcloud)
    saveFile(pcloud, args, sufix='volume_cloud')
    saveFile(pcloud, args, face=face, sufix='volume')

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)
    

if __name__ == '__main__':
    if '-c' in sys.argv:
        if '-t' in sys.argv:
            compare(sys.argv[3], sys.argv[4], True)
        else:
            compare(sys.argv[2], sys.argv[3])
    elif '-e' in sys.argv:
        experiment(sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        files = glob('inputs/*.txt')
        for file_ in files:
            main(file_)
            log('Arquivo '+file_+' lido com sucesso.\n')