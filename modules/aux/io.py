import os.path
import os
import sys
import pcl
from glob import glob
from modules.aux.parser import parseToPointCloud


'Função para remover arquivos .ply antigos'
def removeOldFiles(path):
    files = glob(path+"*")
    for filename in files:
        os.remove(filename)

'Função que printa logs no terminal'
def log(text):
    print('>', text)

'Função para salvar nuvem de pontos em arquivo nos formatos .ply e .pcd'
def saveFile(point_cloud, filename, face=None, sufix=None):
    splited_name = os.path.splitext(os.path.basename(filename))
    if not os.path.exists("outputs/"):
        os.mkdir("outputs/")
    if not os.path.exists("outputs/"+splited_name[0]+"/"):
        os.mkdir("outputs/"+splited_name[0]+"/")
    if sufix:
        path = "outputs/"+splited_name[0]+"/"+sufix+'.ply'
        if sufix == 'original':
            log("Salvando nuvem de pontos original em: "+path)
        elif sufix == 'result':
            log("Salvando nuvem de pontos resultante em: "+path)
        elif sufix == 'surface':
            log("Salvando superfície em: "+path)
    else:
        path = "outputs/"+splited_name[0]+"/"+splited_name[0]+'.ply'
        log("Salvando nuvem de pontos em: "+path)
    if face:
        saveSurface(point_cloud, face, path)
    else:
        point_cloud = parseToPointCloud(point_cloud)
        pcl.save(point_cloud, path)



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
        wr = str(triangle[0])+" "+str(triangle[1])+" "+str(triangle[2])+" "+str(triangle[3])
        f.write(wr+'\n')
    f.close()
