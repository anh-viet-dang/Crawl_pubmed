from os.path import isfile, join
from pdfminer.high_level import extract_text
from lib.scihub import Scihub
from colorama import Fore


def download_with_unfetch_pdf():
    pmid_path = "/home/agent/Documents/AVADA/Crawl_pubmed/data/unfetched_pmid.txt"
    pdf_path = "/home/agent/Documents/AVADA/Crawl_pubmed/data/fetched_pdfs"


    with open(pmid_path, 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')

    for pmid in lines:
        path_save = join(pdf_path, pmid + ".pdf")
        if not isfile(path_save):
            doi = Scihub.pmid2doi(pmid)
            resp_code = Scihub.download_scihub(doi, path_save)
            print(Fore.RED + pmid, ' -> ',Fore.MAGENTA + str(resp_code), ' -> ',Fore.GREEN + doi)


def download_with_cannot_convertpdf():
    pmid_path = r"/home/agent/Documents/AVADA/Crawl_pubmed/data/cannot_convertpdf.txt"
    pdf_path = r"/home/agent/Documents/AVADA/Crawl_pubmed/data/fetched_pdfs"
    

    with open(pmid_path, 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')
    pmids = [p.strip('.txt') for p in lines]

    for pmid in pmids:
        path_pdf = join(pdf_path, pmid + ".pdf")
        try:
            extract_text(path_pdf)
            print(pmid)
            continue
        except:
            doi = Scihub.pmid2doi(pmid)
            resp_code = Scihub.download_scihub(doi, path_pdf)
            print(Fore.RED + pmid, ' -> ',Fore.MAGENTA + str(resp_code), ' -> ',Fore.GREEN + doi)


if __name__ == "__main__":
    download_with_cannot_convertpdf()