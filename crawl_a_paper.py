# /home/agent/anaconda3/bin/python3.9
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urljoin, urlencode, parse_qsl
from lib import send_request
import lib.config as config
from colorama import Fore  # , Back, Style



def find_title(body: Tag) -> str:
    # get title of paper
    title = body.find(name='h1', attrs={"class": "heading-title"})
    return title.get_text().strip()


def find_abstract(body: Tag) -> str:
    # get abstrack of paper
    absTag = body.find(name='div', attrs={"class": "abstract"}, recursive=True)
    if absTag is None:
        # tìm sai keywork trong tag html
        raise Exception("check tag html và key:value trong tìm kiếm")
    else:
        _abstract = absTag.find('p')
        if _abstract is None:
            # NOTE format của đoạn html ko chứa abstract
            r"""
            <div class="abstract">
                <em class="empty-abstract">No abstract available</em>
            </div>
            """
            # trường hợp paper ko có abstract
            msg = absTag.find(
                'em', {"class": "empty-abstract"}, recursive=True)
            print(msg.get_text().strip())
            abstract = ""
        else:
            # NOTE format của đoạn html có chứa abstract
            r"""
            <div class="abstract" id="abstract">
                <h2 class="title">Abstract</h2>
                <div class="abstract-content selected" id="enc-abstract">
                    <p>
                        This article summarizes what is currently known about the 2019 novel
                        coronavirus and offers interim guidance.
                    </p>
                </div>
            </div>
            """
            # trường hợp paper có abstract
            abstract = _abstract.get_text().strip()

    return abstract


def find_similar_article(body: Tag):
    """
        5 url to 5 similar articals and 1 to search 1901 similar articals
    """
    similarTag = body.find_all(
        'a', {"class": "reference-link", "data-ga-category": "reference"}, recursive=True)

    ...


def find_reference_article(body: Tag):
    refTags = body.find_all(
        name='a', attrs={"data-ga-category": "reference"}, recursive=True)
    if refTags is None:
        print("search html with wrong keywords")
    else:
        for refTag in refTags:
            
            ...


def find_cited_by(body: Tag):
    r"""
            <a
              class="usa-button show-all-linked-articles"
              data-href="/?linkname=pubmed_pubmed_citedin&amp;from_uid=32264957"
              data-ga-category="cited_by"
              data-ga-action="show_all"
            >
              See all "Cited by" articles
            </a>
    """
    show_all_cited = body.find('a', {"class": "usa-button show-all-linked-articles",
                               "data-ga-category": "cited_by", "data-ga-action": "show_all"}, recursive=True)

    queryStr = show_all_cited.__getitem__(key= "data-href")  # get query string dẫn đến full cited page of paper
    queryStr = queryStr.strip('/').strip('?')   # BUG bỏ 2 ký tự '/' và '?' để hàm urlencode hoạt động ok

    #https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
    queryDict = dict(parse_qsl(queryStr))                   # convert query String sang dict
    queryDict.update(config.params_cited)                   # thêm key, value cho queryDict
    queryStr = urlencode(queryDict)                         # convert dict sang query string
    queryStr = '/?' + queryStr              # BUG thêm 2 ký tự '/' và '?' để hàm urlencode hoạt động ok


    full_cited_url = urljoin(config.HOMEPAGE, queryStr)     # join homepage and query string thành url hoàn chỉnh
    print(Fore.RED + full_cited_url)

    # parse html ở trang full cited
    resp = send_request(full_cited_url)
    soup = BeautifulSoup(resp.text, "lxml")
    cited_body = soup.find('body', recursive=True)
    

    return full_cited_url


if __name__ == "__main__":
    url = r'https://pubmed.ncbi.nlm.nih.gov/32745377/'
    resp = send_request(url=url)
    soup = BeautifulSoup(resp.text, "lxml")
    # loại bỏ đi các phần header, ... ko liên qua của web
    body = soup.find('body', recursive=True)
    # print(isinstance(body, Tag))  #True

    cited = find_cited_by(body)
    
