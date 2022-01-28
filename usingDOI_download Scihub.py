from os.path import isfile, join

from lib.scihub import Scihub

pmid_path = "/home/agent/Documents/AVADA/Crawl_pubmed/data/unfetched_pmid.txt"
pdf_path = "/home/agent/Documents/AVADA/Crawl_pubmed/data/fetched_pdfs"


with open(pmid_path, 'r', encoding= 'utf-8') as f:
    lines = f.read().strip().split('\n')

for pmid in lines:
    path_save = join(pdf_path, pmid + ".pdf")
    if not isfile(path_save):
        doi = Scihub.pmid2doi(pmid)
        resp_code = Scihub.download_scihub(doi, path_save)
        print(pmid, ' -> ', resp_code, ' -> ', doi)
