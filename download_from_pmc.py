# from lib.pmc import get_tree_from_url
from lib.pmc import get_tree_from_file, get_info_in_tree

# get_tree_from_url()
text = get_tree_from_file()
lines = text.split('\n')


def get_info_in_tree(lines:list[str]) -> list[str]:
    f = open("data/PMC_extract_tree.txt", 'w', encoding= 'utf-8')
    for line in lines:
        list_info = line.split()
        url = list_info[0].strip()
        pmc = ''
        pmid = ''

        for i in list_info[1:]:
            i = i.strip()
            flag_pmc = False
            flag_pmid = False
            if "PMC" in i:
                pmc = i
                flag_pmc = True

            elif "PMID:" in i:
                pmid = i
                flag_pmid = True
            
            if flag_pmc and flag_pmid:
                break
        
        if pmid == '': pmid = r"PMID:"
        if pmc == '': pmc = r"PMC"
        kq = pmid + ' ' + pmc + ' ' + url
        
        f.write(kq + '\n')
        # print(kq)
    f.close()



get_info_in_tree(lines)


