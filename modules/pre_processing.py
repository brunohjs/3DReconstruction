from aux.calc import polar2Cartesian
from aux.files import log

global RANGE
RANGE = 50


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
def splitDataset(dataset):
    log("Separando o dataset em imagens")

    clockwise = False
    data = list()
    image = list()
    previous = dataset[0]['angle']
    for line in dataset[1:]:
        cond_left = line['angle'] < previous and not clockwise
        cond_right = line['angle'] > previous and clockwise
        previous = line['angle']

        if cond_left or cond_right:
            clockwise = not clockwise
            data.append(image)
            image = list()
        image.append(line)
    return data


'Ordenar os beams nas imagens'
def ordenizeDataset(dataset):
    for i in range(len(dataset)):
        if i%2 == 1:
            dataset[i] = dataset[i][::-1]
    return dataset


'Função que coleta o maior valor e a posição de um bin em um beam'
def getHigherBin(dataset):
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
                'dist' : (higher_index+1)*len(beam['raw'])/RANGE,
                'index': higher_index
            }
        if len(image) > 179:
            image.remove(image[-1])
    return dataset


'Refinar o dataset, removendo dados desnecessários e retorna uma nuvem de pontos'
def generatePointCloud(dataset):
    log("Gerando nuvem de pontos")

    refined = list()
    for image in dataset:
        for beam in image:
            x, y = polar2Cartesian(beam['higher']['dist'], beam['angle'])
            refined.append({
                'x'     :   x,
                'y'     :   y,
                'z'     :   beam['z'],
                'value' :   beam['higher']['value']
            })
    return refined