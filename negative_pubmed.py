
import os.path
from random import shuffle

from colorama import Fore

from lib.one_paper import find_abstract, find_title
from lib.utils import pmid2Url, send_request


def get_list_pmid_in_tree(pmc_extract_tree) -> list:
    """
    lấy danh sách pmid trong file pmc_extract tree
    
    """
    with open(pmc_extract_tree, 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')[1:]
    
    pmids = []
    for line in lines:
        pmid = line.split(' ')[0].strip('PMID:').strip()
        if pmid != '':
            pmids.append(pmid)

    shuffle(pmids)
    return pmids


def get_skip_pmid():
    #1 pmid positive = data/pmids.txt + data/similarF1_Feb1.txt
    with open('data/pmids.txt', 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')
    pmid1 = [p.strip() for p in lines]

    with open("data/similarF1_Feb1.txt", 'r', encoding= 'utf-8', errors= 'ignore') as f:
        lines = f.read().strip().split('\n')
    pmid2 = [l.strip() for i, l in enumerate(lines) if i%4==0]
    
    #2 pmid đã crawl trong list negative
    with open("data/negative_Feb1.txt", 'r', encoding= 'utf-8') as f:
        lines = f.read().strip().split('\n')
    pmid3 = [l.strip() for i, l in enumerate(lines) if i%4==0]

    print(Fore.RED +'number of negative pmid = ', len(pmid3))

    #3 pmid 
    return list(set(pmid1 + pmid2 + pmid3)), len(pmid3)

def get_list_keywords():
    with open("data/keyWord_positive.txt", 'r', encoding= 'utf-8') as f:
        keywords = f.read().strip().split('\n')
    list_keyword = [w.strip('.').strip(',').strip(':').lower() for w in keywords]
    return list(set(list_keyword))

class Keyword(object):
    keywords = get_list_keywords()

    @classmethod
    def check_keywords(self, words:str) -> bool:
        words = words.lower()
        for w in self.keywords:
            if w in words:
                # print(Fore.LIGHTGREEN_EX + w)       #FIXME
                return False
        return True

def pmid2info(pmid:str) -> tuple[str, str]:
    full_url = pmid2Url(pmid)
    body = send_request(full_url)
    title = find_title(body)
    abstract = find_abstract(body)
    return title, abstract


if __name__ == "__main__":
    pmc_extract_tree = "data/PMC_extract_tree.txt"
    list_pmid_negative = get_list_pmid_in_tree(pmc_extract_tree)    # list tất cả các pmid lấy từ pmc
    keyword = Keyword()

    negative_data_path = "data/negative_Feb1.txt"
    list_skip_pmid, ccc = get_skip_pmid()
    for pmid in list_pmid_negative:
        if pmid in list_skip_pmid:
            continue
        print(pmid)
        title, abstract = pmid2info(pmid)
        if keyword.check_keywords(title + abstract):
            ccc+=1
            print(ccc, pmid)
            with open(negative_data_path, 'a', encoding= 'utf-8') as f:
                f.write(pmid + '\n'+ title + '\n' + abstract + '\n\n')
                # f.write(title + '\n')
                # f.write(abstract + '\n')
                # f.write('\n')
