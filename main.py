from pre_processing import *

def main():
    'Pré-processamento'
    dataset = getDataset(sys.argv[1])
    dataset = splitDataset(dataset)
    dataset = ordenizeDataset(dataset)
    dataset = getHigherBin(dataset)
    x,y,z,v = transpose(dataset, 1)
    plot3D(x, y, z, v)
    saveFile(x, y, z)

    'Filtragem'



if __name__ == '__main__':
    main()