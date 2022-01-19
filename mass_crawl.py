from crawl_a_paper import (find_abstract, find_cited_by,
                           find_reference_article, find_similar_article,
                           find_title)

from lib import pmid2Url, send_request
from bs4.element import Tag

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


def get_list_pmid(path=r"data/pmid_gene.txt") -> list:
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
    



if __name__ == "__main__":
    list_pmids = get_list_pmid()
    for pmid in list_pmids:
        url_pmid = pmid2Url(pmid)
        body_paper = send_request(url_pmid)
        title = find_title(body_paper)
