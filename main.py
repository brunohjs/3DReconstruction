import sys
import time
from glob import glob

from modules.aux.io import *
from modules.aux.global_vars import *

from modules.pre_processing import *
from modules.filtering import *
from modules.reconstruction import *
from modules.comparison import *


def compare(c1_path, c2_path):
    t0 = time.time()

    removeOldFiles([c1_path, c2_path], True)

    'Carregar arquivos das nuvens de pontos'
    cloud1 = plyToCloud(c1_path+'/result.ply')
    cloud2 = plyToCloud(c2_path+'/result.ply')

    'Comparar'
    pcloud_result = comparison(cloud1, cloud2)
    pcloud_result = staticalOutlierFilter(pcloud_result)

    'Reconstrução'
    pcloud, face = reconstruct(cloud1)
    saveFile(pcloud, [c1_path, c2_path], face=face, sufix=getNamePath(c1_path)+'_surface', comparison=True)
    pcloud, face = reconstruct(cloud2)
    saveFile(pcloud, [c1_path, c2_path], face=face, sufix=getNamePath(c2_path)+'_surface', comparison=True)
    pcloud, face = reconstruct(pcloud_result)
    saveFile(pcloud, [c1_path, c2_path], face=face, sufix='surface', comparison=True)

    saveFile(cloud1, [c1_path, c2_path], sufix=getNamePath(c1_path), comparison=True)
    saveFile(cloud2, [c1_path, c2_path], sufix=getNamePath(c2_path), comparison=True)
    saveFile(pcloud_result, [c1_path, c2_path], comparison=True)

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
    saveFile(pcloud, args, sufix='filt1')
    pcloud = staticalOutlierFilter(pcloud)
    saveFile(pcloud, args, sufix='filt2')
    pcloud = smoothingFilter(pcloud)
    saveFile(pcloud, args, sufix='filt3')
    pcloud = downsamplerFilter(pcloud, space=1)
    saveFile(pcloud, args, sufix='result')

    'Reconstrução'
    pcloud, face = reconstruct(pcloud)
    saveFile(pcloud, args, face=face, sufix='surface')

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)
    

if __name__ == '__main__':
    if '-c' in sys.argv:
        compare(sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        files = glob('inputs/*.txt')
        for file_ in files:
            try:
                main(file_)
                log('Arquivo '+file_+' lido com sucesso.\n')
            except:
                log('Erro ao ler o arquivo '+file_+'\n')