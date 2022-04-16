from os.path import join
from os import listdir

from colorama import Fore

from lib.scihub import SciHub
from lib.config import PMID2DOI_FILE_PATH, PMID_HGMD, PMID_SIMI, PMID_NEGA


folder_save_pdf = "data/fulltext/fetched_pdfs"
def get_crawled_pmid() -> list:
    return set([pdf.strip('.pdf') for pdf in listdir(folder_save_pdf) if pdf.endswith('.pdf')])


def get_all_pmid() -> list:
    with open('data/pmids.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    return [p.strip() for p in lines]
    # return pmids

if __name__ == "__main__":
    sh = SciHub()
    
    all_pmids = get_all_pmid()
    pmided = get_crawled_pmid()
    for pmid in all_pmids:
        if pmid in pmided:
            continue
        
        try:
            doi = SciHub.pmid2doi(pmid)     #   10.1200/JCO.2005.02.093
            if doi != "":
                pdf_path_save = join(folder_save_pdf, pmid + '.pdf')
                size_pdf = sh.download(doi, folder_save_pdf, pdf_path_save)
                if size_pdf != 0:
                    print("download success ", pdf_path_save)
            else:
                print(Fore.RED, "download fail because doi = ''", Fore.RESET)

        except Exception as e:
            print(e)