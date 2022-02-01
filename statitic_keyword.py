from collections import Counter

#NOTE
r"""
thống kê, tìm các keyword phổ biến trong title, abstract

"""
pmid_path = "data/pmids.txt"
# pmid_simi_path = "data/similarF1.txt"

path_info = "data/info_paper.txt"
with open(path_info, 'r', encoding='utf-8') as f:
    lines = f.read().strip().split('\n')

def stat_title():
    titles = [l for i, l in enumerate(lines) if i%4 == 1]
    words_title = []
    for tit in titles:
        words_title += tit.strip().split()

    statitic_title = Counter(words_title)
    statitic_title = dict(sorted(statitic_title.items(), key=lambda item: item[1], reverse= False))
    f = open("data/keyword_title.txt", 'w', encoding= 'utf-8')
    for k, v in statitic_title.items():
        f.write(k + ' ' + str(v) + '\n')
    f.close()

def stat_abstract():
    abstracts = [l for i, l in enumerate(lines) if i%4 == 2]
    words_abstract = []
    for abs in abstracts:
        words_abstract += abs.strip().split()

    statitic_abstract = Counter(words_abstract)
    statitic_abstract = dict(sorted(statitic_abstract.items(), key=lambda item: item[1], reverse= False))
    f = open("data/keyword_abstract.txt", 'w', encoding= 'utf-8')
    for k, v in statitic_abstract.items():
        f.write(k + ' ' + str(v) + '\n')
    f.close()


def filter_keyword():
    with open("data/keyword_title.txt", 'r', encoding= 'utf-8') as f:
        keywords = f.read().strip().split('\n')
    keywords_title = keywords


    with open("data/keyword_abstract.txt", 'r', encoding= 'utf-8') as f:
        keywords = f.read().strip().split('\n')
    keywords_abstract = keywords

    new_words = [w for w in keywords_abstract if w not in keywords_title]
    with open("data/filter_keyword_abstract.txt", 'w', encoding= 'utf-8') as f:
        f.write('\n'.join(new_words) + '\n')

if __name__ == "__main__":
    # stat_abstract()
    # stat_title()
    filter_keyword()