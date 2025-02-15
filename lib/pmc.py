from os.path import getsize, isfile

import requests

from .config import PMC as pmc_fth
from .utils import send_request

# from bs4 import BeautifulSoup
# from bs4.element import Tag


class PMC(object):
    r"""
    còn nhiều bug, chưa dùng đc
    """
    url = r"https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_non_comm_use_pdf.txt"
    path_save = r"data/PMC_tree.txt"
    def __init__(self):
        self.fulltext = self.get_tree_from_url()
        self.list_path = self.getTree_from_text()

    @classmethod
    def get_tree_from_url(self):
        body = send_request(self.url)
        self.fulltext = body.get_text(strip= True).strip()
        with open (self.path_save, 'w', encoding= "utf-8") as f:
            f.write(self.fulltext)
        return self
    
    @classmethod
    def getTree_from_text(self):
        with open(self.path_save, 'r', encoding= 'utf-8') as f:
            self.list_path = f.read().strip().split('\n')
        return(self)


url = r"https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_non_comm_use_pdf.txt"
path_save = r"data/PMC_tree.txt"


def get_tree_from_url() -> str:
    r"""
    download all tree path of PMC
    """
    body = send_request(url)
    text = body.get_text(strip= True).strip()
    with open (path_save, 'w', encoding= "utf-8") as f:
        f.write(text)
    return text

def get_tree_from_file(path_save) -> str:
    r"""
    read full text from path
    """
    with open(path_save, 'r', encoding= 'utf-8') as f:
        text = f.read().strip()
    return text


class PMC_tree(object):
    data = []
    
    def __init__(self) -> None:
        with open('data/PMC_extract_tree.txt', 'r', encoding= 'utf-8') as f:
            lines = f.read().strip().split('\n')[1:]
        
        # self.data = []
        for line in lines:
            line = line.split(' ')
            pmid = line[0][5:].strip()
            pmc = line[1].strip()
            oa_pdf = line[2].strip()
            self.data.append((pmid, pmc, oa_pdf))

    @classmethod
    def find_oa_PDF_from_pmid(self, pmid:str) -> str:
        """
        input pmid:str
        dựa vào file    data/PMC_extract_tree.txt để tìm
        return PMC
        """
        for line in self.data:
            if line[0] == pmid.strip():
                return line[2]
        return None


    @staticmethod
    def download_PMC(oa_pdf:str, path_save:str) -> tuple:
        """ ví dụ:
            oa_pdf = r"oa_pdf/8d/22/20020509.PMC1193645.pdf"  # path lấy từ PMC_tree.txt
            download từ url     https://ftp.ncbi.nlm.nih.gov/pub/pmc/
        """

        resp = requests.get(pmc_fth + oa_pdf)
        status_code = resp.status_code
        if status_code == 200:
            with open(path_save, 'wb') as f:
                f.write(resp.content)

        if isfile(path_save):   return status_code, getsize(path_save)
        else:                   return status_code, 0


if __name__ == "__main__": ...
