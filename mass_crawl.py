import os

from bs4.element import Tag
from colorama import Fore

from crawl_a_paper import find_abstract, find_title
from lib.utils import pmid2Url, send_request

"""
Từ pmid đã có, thực hiện tìm pmid similar, cited, reference
if tìm xem trong list pmid gene/not gene đã có chưa, nếu có:
    bỏ qua
elif classfication (title, abstract):
    liên quan đến gen 
        -> đưa qua queue download
        -> them vào pmid gene
        -> search tiếp similar, cited, ref để lấy pmid, title, abstract
    ko liên quan đến gen 
        -> add vào not gene

# search theo hường BFS, build graph search, tránh recursive
# lần đầu download theo hướng liên quan đến gene trước
"""


def get_list_pmid(path=r"data/pmids.txt") -> list:
    f = open(path, 'r')
    pmids = f.read().strip().split('\n')
    f.close()

    if len(pmids) != 0:
        return pmids
    else:
        raise "not found pmid"

def find_info_paper(body:Tag)->tuple:
    title = find_title(body)
    abstract = find_abstract(body)
    return title, abstract

def get_info_from_pmid():

    r"""
    thu thập thông tin về title, abstract 
    từ các pmid đã biết từ trước
    danh sách pmid lấy từ data/pmid_gene.txt
    kết quả đc lưu ở data/Pmid_title_abstract.txt
    """

    path = "data/info_paper.txt"
    if os.path.isfile(path):
        with open(path, 'r') as f:
            _pmids = f.read().strip().split('\n')
        pmided = [pid for i, pid in enumerate(_pmids) if i%4 == 0]  #list pmid đã crawl
    else: 
        pmided = []

    list_pmids = get_list_pmid()    
    pmid_continue = []  # list pmid chưa crawl
    for pid in list_pmids:
        if pid not in pmided:
            pmid_continue.append(pid)

    f = open(path, 'a', encoding= 'utf-8')
    for pmid in pmid_continue:
        url_pmid = pmid2Url(pmid)       # get full url
        body_paper = send_request(url_pmid)     # requests
        title, abstract = find_info_paper(body_paper)   # get info

        print(Fore.RED + pmid)
        print(Fore.CYAN + title)
        print(Fore.LIGHTMAGENTA_EX + abstract)

        f.write(pmid + '\n' + title + '\n' + abstract + '\n')
        f.write('\n')
    f.close()


if __name__ == "__main__":
    get_info_from_pmid()
