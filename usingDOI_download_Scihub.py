"""
dùng doi để download fulltext từ scihub
"""
from os.path import isfile, join
import os
from pdfminer.high_level import extract_text
from lib.scihub import Scihub
from colorama import Fore
from lib.config import PMID2DOI_FILE_PATH, PMID_HGMD, PMID_SIMI, PMID_NEGA

folder_save_pdf = "data/fulltext/fetched_pdfs"

def get_list_pmid(path:str) -> list:
    """
    load file crawl title, abstract để lấy pmid
    """
    with open(path, 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')
    
    pmids = []
    for i, line in enumerate(lines):
        if i%4 == 0:
            if not line.isdecimal():
                print(Fore.CYAN + str(i), Fore.BLUE + line)  #PMID
                print(Fore.RED + lines[i+1])
                print(Fore.LIGHTGREEN_EX + lines[i+2])
                exit()
            pmids.append(line.strip())

    return pmids


def download_fulltext(pmid:str):
    doi = Scihub.pmid2doi(pmid, is_save= True)
    if doi != "":
        pdf_path_save = join(folder_save_pdf, pmid + '.pdf')
        sttcode = Scihub.download_scihub(doi= doi, path_save=pdf_path_save)
        return sttcode, doi
    else:
        return 0, doi

def get_crawled_fulltext_pmid():
    return [pdf.strip('.pdf') for pdf in os.listdir(folder_save_pdf) if pdf.endswith('.pdf')]


if __name__ == "__main__":
    pmid_hgmd = get_list_pmid(PMID_HGMD)
    pmid_similar = get_list_pmid(PMID_SIMI)
    pmid_negative = get_list_pmid(PMID_NEGA)

    pmid_crawls = get_crawled_fulltext_pmid()
    for pmid in pmid_hgmd:
        if pmid in pmid_crawls: continue

        sttcode, doi = download_fulltext(pmid)
        if sttcode != 200:
            print(Fore.RED + pmid + ' ' + Fore.LIGHTMAGENTA_EX + str(sttcode) + ' ' +Fore.LIGHTGREEN_EX + doi )
