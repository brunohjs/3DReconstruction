import sys
from pre_processing import *
from filtering import *
from modules.files import saveFile

def main():
    
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
    
    'Salvar em arquivo'
    saveFile(point_cloud)
    

if __name__ == '__main__':
    main()