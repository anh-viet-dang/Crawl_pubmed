# chia nhỏ folder to thành nhiều folder nhỏ hơn
import os, shutil
from glob import glob
from colorama import Fore
from os.path import join, isfile


def split_data(folder:str, subfolderName:str = 'sub',num_of_subfold:int = 12, ext:str = '.pdf'):
    r"""
    chia data bên trong folder data thành nhiều subfolder
    """

    def move_data2Subfolder(pdfs:list, dst:str):
        if not os.path.isdir(dst):
            os.makedirs(dst)

        for pdf in pdfs:
            shutil.move(pdf, dst)
    

    # create list subfolder
    subfolds = [join(folder, '{}{}'.format(subfolderName,sf)) for sf in range(num_of_subfold)]
    datas = glob(folder + '{}*{}'.format(os.sep, ext))

    # num_data_in_each_sub
    total_data = len(datas)
    num = total_data // num_of_subfold + 1

    for i in range(num_of_subfold):
        move_data2Subfolder(datas[num*i : min(num*(i+1), total_data)], 
                            subfolds[i])


def merge_data(folder:str):
    for root, _ , files in os.walk(folder):
        for file in files:
            if not isfile(join(folder, file)):
                path = join(root, file)
                shutil.move(path, folder)
        
        if len(os.listdir(root)) == 0:
            os.removedirs(root)


def count_data(folder:str) -> int:
    c:int = 0
    pmid = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file not in pmid:
                pmid.append(file)
                c+=1
            else:
                path = os.path.join(root, file)
                print(path)
                # os.remove(path)

    print(c)
    return c

def find_size(folder:str):
    t_size = 50*2**20
    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            size = os.path.getsize(path)
            if size >= t_size:
                print(path, size/2**20)

if __name__ == "__main__":
    ...