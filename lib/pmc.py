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

def get_tree_from_file() -> str:
    r"""
    read full text from path
    """
    with open(path_save, 'r', encoding= 'utf-8') as f:
        text = f.read().strip()
    return text


def get_info_in_tree(lines:list[str]) -> list:
    for line in lines:
        infos = line.split()
        