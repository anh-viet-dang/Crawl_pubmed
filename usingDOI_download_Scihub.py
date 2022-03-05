"""
dùng doi để download fulltext từ scihub
"""
from os.path import join, getsize
from os import listdir
from colorama import Fore

from lib.scihub import SciHub
from lib.config import PMID2DOI_FILE_PATH, PMID_HGMD, PMID_SIMI, PMID_NEGA

folder_save_pdf = "data/fulltext/similar_pdfs"

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


def get_crawled_fulltext_pmid() -> tuple:
    # lấy danh sách paper và maxsize đã download full path
    total_size = 0
    pmids = []
    for pdf in listdir(folder_save_pdf):
        if pdf.endswith('.pdf'):
            total_size += getsize( join( folder_save_pdf, pdf))
            pmids.append(pdf.strip('.pdf'))

    # return [pdf.strip('.pdf') for pdf in os.listdir(folder_save_pdf) if pdf.endswith('.pdf')]
    return pmids, total_size


def get_pmid_sent_request() -> list:
    # đọc file PMID2DOI_FILE_PATH trong config để lấy pmid đã sent_request

    with open(PMID2DOI_FILE_PATH, 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')

    newlines = []
    pmids = []
    for line in lines:
        pmid = line.split(',')[0].strip()
        if pmid not in pmids:
            pmids.append(pmid)      # return
            newlines.append(line)   # record in csv file
    
    with open(PMID2DOI_FILE_PATH, 'w', encoding= 'utf-8') as f:
        f.write('\n'.join(newlines) + '\n')
    
    return pmids


if __name__ == "__main__":
    # pmid_hgmd = get_list_pmid(PMID_HGMD)
    pmid_similar = get_list_pmid(PMID_SIMI)
    # pmid_negative = get_list_pmid(PMID_NEGA)


    max_size = round(40* 2**30) 
    sh = SciHub()
    pmid_crawls, size = get_crawled_fulltext_pmid() # pmid đã craws và size 
    pmid_crawls = set(pmid_crawls + get_pmid_sent_request())
    print(Fore.RED + "size = %.2f Gigabytes" % size/2**30 + Fore.RESET)

    # duyệt qua từng pmid để download
    for pmid in pmid_similar:
        if pmid in pmid_crawls:
            # bỏ qua pmid đã send request, tìm chúng trong danh sách doi
            # bỏ qua pmid đã crawl xong pdf
            continue

        # implement download from pmc
        # elif download from pubmed

        # else download from scihub(using doi)
        try:
            doi = SciHub.pmid2doi(pmid)     #   10.1200/JCO.2005.02.093
            if doi != "":
                pdf_path_save = join(folder_save_pdf, pmid + '.pdf')

                size_pdf = sh.download(doi, folder_save_pdf, pdf_path_save)
                if size_pdf != 0:
                    print("download success ", pdf_path_save)

                    # check dừng crawl vì full ổ cứng
                    size += size_pdf
                    if size >= max_size:
                        # dừng crawl vì full dung lượng ổ cứng
                        print("stop crawling because of SSD is full", size/2*30)
                        break
        except Exception as e:
            print(e)
