from modules.aux.parser import polar2Cartesian
from modules.aux.io import log


'Pegar o dataset do arquivo texto'
def getDataset(file):
    log("Coletando dados do dataset")

    dataset = list()
    f = open(file)
    for line in f.readlines()[1:]:
        aux = line.rstrip().split(',')
        beam = {
            'id': int(aux[0]),
            'angle': float(aux[1]),
            'x': float(aux[2]),
            'y': float(aux[3]),
            'z': float(aux[4]),
            'ox': float(aux[5]),
            'oy': float(aux[6]),
            'oz': float(aux[7]),
            'ow': float(aux[8]),
            'raw': aux[9:-1]
        }
        for i in range(len(beam['raw'])):
            beam['raw'][i] = float(beam['raw'][i])
        dataset.append(beam)
    return dataset


'Separar o dataset em imagens'
def splitDataset(dataset, image_size=180):
    log("Separando o dataset em imagens")

    if dataset[0]['angle'] < dataset[1]['angle']:
        clockwise = False
    else:
        clockwise = True
    data = list()
    image = list()
    previous = dataset[0]['angle']
    for line in dataset:
        cond_left = line['angle'] < previous and not clockwise
        cond_right = line['angle'] > previous and clockwise
        previous = line['angle']
        if cond_left or cond_right:
            clockwise = not clockwise
            if len(image) == image_size:
                data.append(image)
            image = list()
        image.append(line)
    data.append(image)
    return data


'Ordenar os beams nas imagens'
def ordenizeDataset(dataset):
    for i in range(len(dataset)):
        if i%2 == 1:
            dataset[i] = dataset[i][::-1]
    return dataset


'Função que coleta o maior valor e a posição de um bin em um beam'
def getHigherBin(dataset, range_bin, image_size=179):
    log("Coletando os maiores bins dos beams")

    for image in dataset:
        for beam in image:
            higher = 0
            higher_index = -1
            for bin_ in beam['raw']:
                if bin_ > higher:
                    higher = bin_
                    higher_index = beam['raw'].index(bin_)
            beam['higher'] = {
                'value': higher, 
                'dist' : (higher_index+1)/len(beam['raw'])*range_bin,
                'index': higher_index
            }
        if len(image) > image_size:
            image.remove(image[-1])
    return dataset


def getHigherBins(dataset, range_bin=60, nbeams=10):
    log("Coletando os maiores bins dos beams")

    new_dataset = list()
    for image in dataset:
        new_dataset.append(list())
        for beam in image:
            highers = list()
            for i, bin_ in enumerate(beam['raw']):
                if len(highers) < nbeams:
                    highers.append((bin_, i))
                else:
                    for j in range(len(highers)):
                        if bin_ > highers[j][0]:
                            highers[j] = (bin_, i)
                            break
            for i in range(len(highers)):
                aux = dict()
                aux['angle'] = beam['angle']
                aux['z'] = beam['z']
                aux['higher'] = dict()
                aux['higher']['value'] = highers[i][0]
                aux['higher']['dist'] = (highers[i][1]+1)/len(beam['raw'])*range_bin
                aux['higher']['index'] = highers[i][1]
                new_dataset[-1].append(aux)
    return new_dataset


'Refinar o dataset, removendo dados desnecessários e retorna uma nuvem de pontos'
def generatePointCloud(dataset):
    log("Gerando nuvem de pontos")

    refined = list()
    for image in dataset:
        for beam in image:
            x, y = polar2Cartesian(beam['higher']['dist'], beam['angle'])
            refined.append({
                'x':   x,
                'y':   y,
                'z':   beam['z'],
                'value':   beam['higher']['value'],
                'angle':   beam['angle'],
                'dist': beam['higher']['dist']
            })
    return refined