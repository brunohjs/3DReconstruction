import os.path
import os
import sys
import pcl
from glob import glob
from modules.aux.parser import parseToPointCloud


def removeOldFiles(path):
    files = glob(path+"*")
    for filename in files:
        os.remove(filename)

'Função que printa logs no terminal'
def log(text):
    print('>', text)

'Função para salvar nuvem de pontos em arquivo nos formatos .ply e .pcd'
def saveFile(point_cloud, filename, sufix=None, ftype='.ply', type_="current"):
    splited_name = os.path.splitext(os.path.basename(filename))
    if not os.path.exists("outputs/"):
        os.mkdir("outputs/")
    if not os.path.exists("outputs/"+splited_name[0]+"/"):
        os.mkdir("outputs/"+splited_name[0]+"/")
    if sufix:
        path = "outputs/"+splited_name[0]+"/"+sufix+ftype
        if sufix == 'original':
            log("Salvando nuvem de pontos original em: "+path)
        elif sufix == 'result':
            log("Salvando nuvem de pontos resultante em: "+path)
    else:
        path = "outputs/"+splited_name[0]+"/"+splited_name[0]+ftype
        log("Salvando nuvem de pontos em: "+path)

    point_cloud = parseToPointCloud(point_cloud)
    pcl.save(point_cloud, path)