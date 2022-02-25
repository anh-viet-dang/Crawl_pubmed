PUBMED = r"https://pubmed.ncbi.nlm.nih.gov/"
PMC = r"https://ftp.ncbi.nlm.nih.gov/pub/pmc/"
SCIHUB = r"https://sci-hub.se/"


params_query = {
'show_snippets':'off',
'format':'pubmed',
'size': '200'
}

PMID2DOI_FILE_PATH = r"data/pmid2doi.csv"

#positive
PMID_HGMD = "data/info_paper.txt"
PMID_SIMI = "data/similarF1_Feb1.txt"

# negative
PMID_NEGA = "data/negative_Feb1.txt"

if __name__ == "__main__":...
