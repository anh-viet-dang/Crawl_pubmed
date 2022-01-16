#/home/agent/anaconda3/bin/python3.9
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from colorama import Fore
r"""
    Từ response của request có query &format=pubmed
    #    r"https://pubmed.ncbi.nlm.nih.gov/trending/?format=pubmed&size=200"
    #   "https://pubmed.ncbi.nlm.nih.gov/?show_snippets=off&format=pubmed&size=200&linkname=pubmed_pubmed_citedin&from_uid=32745377"


    phân tích html để lấy thông tin về 200 paper

    Chia nhỏ thành từng phần 1, mỗi phần là 1 paper
    Từ đó lấy ra 3 trường thông tin
    PMID : cho download full text
    title: classify
    abstract: classify
"""

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
]

from random import choice
def random_headers(User_Agent:list= desktop_agents):
    return {'User-Agent': choice(User_Agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def send_request(url: str):
    return requests.get(url=url, headers=random_headers())


url = r"https://pubmed.ncbi.nlm.nih.gov/?linkname=pubmed_pubmed&from_uid=32745377&show_snippets=off&format=pubmed&size=200"
req = requests.get(url=url, headers=random_headers())

soup = BeautifulSoup(req.text, "lxml")
body = soup.find('body')
# text = body.get_text().strip()

# papers = text.split('\nPMID- ')


def split_info(info_one_paper: str):
    r"""
         ____________________________________________________
        |.==================================================,|
        ||  Chia nhỏ thông tin trên paper thành các dòng    ||
        ||  if char đầu dòng là khoảng trắng:               ||
        ||      ghép dòng đó vào dòng phía trên nó.         ||
        ||  else:                                           ||
        ||      Tạo dòng mới                                ||
        ||  Ghép các trường thông tin lại với nhau          ||
        ||  Tìm trường thông tin theo 7 char đầu tiên       ||
        ||     .~~~~.                                       ||
        ||   / ><    \  //                                  ||
        ||  |        |/\                                    ||
        ||   \______//\/                                    ||
        ||   _(____)/ /                                     ||
        ||__/ ,_ _  _/______________________________________||
        '===\___\_) |========================================'
             |______|
             |  ||  |
             |__||__|
             (__)(__)
    """
    
    lines = info_one_paper.strip().split('\n')
    list_info = []      # list chứa các trường thông tin
    info = [lines[0]]   # thông tin của 1 trường, ví dụ PMID- 35025605
    for line in lines[1:]:
        if line[0] == ' ':
            info.append(line.strip())
        else:
            list_info.append(' '.join(info))
            info.clear()
            info.append(line.strip())
    list_info.append(' '.join(info))

    return list_info

def get_from_format_pubmed(body:Tag):
    """
    Lấy thông tin PMID, title, abstract từ respond có query &format=pubmed
    Tạm thời áp dụng cho 

    ví dụ: https://pubmed.ncbi.nlm.nih.gov/?linkname=pubmed_pubmed_citedin&from_uid=32745377&show_snippets=off&format=pubmed&size=200
    trending, reference, cited by
    """
    text = body.get_text().strip()
    papers = text.split('\nPMID- ')

    list_info_paper = []
    for paper in papers:

        # Do split('\nPMID- ') nên từ paper thứ 2 trở đi bị mất string "\nPMID- "
        # Cần check và bổ sung thêm
        if not paper.startswith(r"PMID- "):
            paper = r"PMID- " + paper
        
        list_info = split_info(paper)

        tong:int = 0
        pmid = ''
        title = ''
        abstract = ''
        
        for info in list_info:
            if info.startswith(r"PMID- ") and pmid == '':
                pmid = info[6:]#; print(r"PMID- ", pmid)
                tong += 1

            elif info.startswith(r"TI  - ") and title == '': 
                title = info[6:]#; print(r"TI  - ", title)
                tong += 1

            elif info.startswith(r"AB  - ") and abstract == '': 
                abstract = info[6:]#; print(r"AB  - ", abstract)
                tong += 1
            
            if tong == 3: break
            # elif tong > 3:
            #     msg = r"Nhiều hơn 3 trường thông tin, kiểm tra lại các trường tt trong paper"
            #     raise Exception(msg)
        list_info_paper.append([pmid, title, abstract])

    return list_info_paper


if __name__ == "__main__":
    papers = get_from_format_pubmed(body)
    for paper in papers:
        with open('paper/' + paper[0] + ".txt", 'w') as f:
            for i in paper:
                f.write(i + '\n')