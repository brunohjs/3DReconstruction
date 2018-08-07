import sys
import time
import glob

from modules.aux.io import saveFile, log

from modules.pre_processing import *
from modules.filtering import *
from modules.reconstruction import *
from modules.comparison import *



def main(args):
    t0 = time.time()

    'Pré-processamento'
    dataset = getDataset(args)
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset)
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
    saveFile(pcloud, args, sufix='filt4')

    'Reconstrução'
    pcloud, face = reconstruct(pcloud)

    'Comparação'
    #pcloud_result = comparison(pcloud, pcloud_original)

    'Salvar em arquivo'
    saveFile(pcloud, args, face=face, sufix='surface')

    t1 = time.time()
    dt = str(round(t1 - t0, 2))+'s'
    log('Processo finalizado. Tempo total: '+dt)
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        files = glob.glob('inputs/*.txt')
        for file_ in files:
            main(file_)
            log('Arquivo '+file_+' lido com sucesso.\n')
            #except:
                #log('Erro ao ler o arquivo '+file_)