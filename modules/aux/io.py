import os.path
import os
import sys
import pcl
from glob import glob
from plyfile import PlyData
from modules.aux.parser import parseToPointCloud


'Função que retira o nome do arquivo'
def getNamePath(path):
    if type(path) is list and len(path) > 1:
        splited_name = list()
        for p in path:
            splited_name.append(p.split('/'))
            if splited_name[-1][-1] == '':
                splited_name[-1] = splited_name[-1][-2]
            else:
                splited_name[-1] = splited_name[-1][-1]
    else:
        splited_name = path.split('/')
        if splited_name[-1] == '':
            splited_name = splited_name[-2]
        else:
            splited_name = splited_name[-1]
        if splited_name[-4:] in ('.txt', '.ply'):
            splited_name = splited_name[:-4]
    return splited_name


'Função para remover arquivos .ply antigos'
def removeOldFiles(path, comparison=False):
    log('Deletando arquivos antigos')

    splited_name = getNamePath(path)
    if comparison:
        splited_name = '_'.join(splited_name)
        files = glob("outputs/comparisons/"+splited_name+"/*")
    else:
        files = glob("outputs/surfaces/"+splited_name+"/*")
    for filename in files:
        os.remove(filename)


'Função que printa logs no terminal'
def log(text):
    print('>', text)


'Função para salvar nuvem de pontos em arquivo nos formatos .ply e .pcd'
def saveFile(point_cloud, filename=None, face=None, sufix=None, comparison=False):
    if filename:
        if comparison:
            splited_name = getNamePath(filename)
            splited_name = '_'.join(splited_name)
            
            if not os.path.exists("outputs/comparisons/"):
                os.mkdir("outputs/comparisons/")
            if not os.path.exists("outputs/comparisons/"+splited_name+"/"):
                os.mkdir("outputs/comparisons/"+splited_name+"/")
            if sufix:
                path = "outputs/comparisons/"+splited_name+"/"+sufix+'.ply'
            else:
                path = "outputs/comparisons/"+splited_name+"/result.ply"
        else: 
            splited_name = getNamePath(filename)  
            
            if not os.path.exists("outputs/"):
                os.mkdir("outputs/")
            if not os.path.exists("outputs/surfaces/"):
                os.mkdir("outputs/surfaces/")
            if not os.path.exists("outputs/surfaces/"+splited_name+"/"):
                os.mkdir("outputs/surfaces/"+splited_name+"/")
            if sufix:
                path = "outputs/surfaces/"+splited_name+"/"+sufix+'.ply'
                if sufix == 'original':
                    log("Salvando nuvem de pontos original em: "+path)
                elif sufix == 'result':
                    log("Salvando nuvem de pontos resultante em: "+path)
                elif sufix == 'surface':
                    log("Salvando superfície em: "+path)
            else:
                path = "outputs/surfaces/"+splited_name+"/"+splited_name+'.ply'
                log("Salvando nuvem de pontos em: "+path)
        if face:
            saveSurface(point_cloud, face, path)
        else:
            point_cloud = parseToPointCloud(point_cloud)
            pcl.save(point_cloud, path)
    else:
        if face:
            saveSurface(point_cloud, face, 'teste_'+sufix+'.ply')
        else:
            point_cloud = parseToPointCloud(point_cloud)
            pcl.save(point_cloud, 'teste_'+sufix+'.ply')


'Função que salva a superfície em um arquivo .ply'
def saveSurface(vertex, face, path):
    f = open(path, 'w')

    header = "ply\n"   
    header += "format ascii 1.0\n"
    header += "element vertex "+str(len(vertex))+"\n"
    header += "property float x\n"
    header += "property float y\n"
    header += "property float z\n"
    header += "element face "+str(len(face))+"\n"
    header += "property list uchar int vertex_index\n"
    header += "end_header\n"
    
    f.write(header)
    for point in vertex:
        wr = str(point[0])+" "+str(point[1])+" "+str(point[2])
        f.write(wr+'\n')
    for triangle in face:
        wr = str(3)+" "+str(triangle[0])+" "+str(triangle[1])+" "+str(triangle[2])
        f.write(wr+'\n')
    f.close()


'Função para converter um arquivo .ply pra um objeto do tipo Nuvem de Pontos'
def plyToCloud(path):
    log('Carregando nuvem de pontos em: '+path)

    point_cloud = list()
    for point in PlyData.read(path).elements[0].data:
        point_cloud.append([float(point[0]), float(point[1]), float(point[2])])
    point_cloud = parseToPointCloud(point_cloud)
    return point_cloud

'Função para converter um arquivo .ply para uma lista'
def plyToList(path):
    log('Carregando nuvem de pontos em: '+path)
    vertex = list()
    face = list()
    for point in PlyData.read(path).elements[0].data:
        vertex.append([float(point[0]), float(point[1]), float(point[2])])
    for point in PlyData.read(path).elements[1].data:
        face.append([int(point[0][0]), int(point[0][1]), int(point[0][2])])
    return vertex, face