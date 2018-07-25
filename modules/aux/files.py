import os.path
import os
import sys
import pcl
from aux.parser import parseToPointCloud


'Função que printa logs no terminal'
def log(text):
    print('>', text)

'Função para salvar nuvem de pontos em arquivo nos formatos .ply e .pcd'
def saveFile(point_cloud, filename=None, ftype='.ply', type_="current"):
    if not os.path.exists("../outputs/"):
        os.mkdir("../outputs/")
    if filename:
        path = "../outputs/" + filename
    else:
        splited_name = os.path.splitext(os.path.basename(sys.argv[1]))
        if type_ == 'original':
            path = "../outputs/" + splited_name[0] + '_original' + ftype
            log("Salvando nuvem de pontos original em: "+path)
        elif type_ == 'result':
            path = "../outputs/" + splited_name[0] + '_result' + ftype
            log("Salvando nuvem de pontos resultante em: "+path)
        else:
            path = "../outputs/" + splited_name[0] + ftype
            log("Salvando nuvem de pontos em: "+path)

    point_cloud = parseToPointCloud(point_cloud)
    pcl.save(point_cloud, path)