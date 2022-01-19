# /home/agent/anaconda3/bin/python3.9
from urllib.parse import urljoin

from bs4.element import Tag
from colorama import Fore  # , Back, Style

from lib import add_query, send_request
from lib.config import HOMEPAGE


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


def find_reference_body(body: Tag)->Tag:
    r"""
        >>> input body html của HOMEPAGE/pmid
        >>> return body của page chứa full references paper

        format tag html cần tìm
                  <button
                aria-controls="top-references-list-1"
                class="show-all"
                data-ga-action="show_more"
                data-ga-category="reference"
                data-next-page-url="/32264957/references/"
                ref="linksrc=show_all_references_link"
              >
                Show all 19 references
              </button>
    """

    show_all_ref = body.find('button', {"aria-controls": "top-references-list-1",
                                        "class": "show-all", "data-ga-action": "show_more",
                                        "data-ga-category": "reference"}, recursive=True)

    nextPageUrl = show_all_ref.__getitem__(key="data-next-page-url")    # "/32264957/references/"

    # ref paper ko theo format nên ko dùng func add_query
    full_ref_url = urljoin(HOMEPAGE, nextPageUrl)
    ref_body = send_request(full_ref_url)


    # <ol class="references-list" id="full-references-list-1">
    ol = ref_body.find('ol', {"class":"references-list"}, recursive= True)

    return ol


def find_similar_body(body: Tag)->Tag:
    """
        5 url to 5 similar articals and 1 to search 1901 similar articals
    """
    see_allSimilarTag = body.find('a', {"class": "usa-button show-all-linked-articles", 
                                             "data-ga-action": "show_all", 
                                             "data-ga-category": "similar_article"}, recursive=True)

    queryStr = see_allSimilarTag.__getitem__(key="data-href")   #"/?linkname=pubmed_pubmed&amp;from_uid=32264957"
    full_Similar_url = add_query(queryStr)
    body = send_request(full_Similar_url)

    return body


def find_cited_body(body: Tag)->Tag:
    r"""
    input: body của paper
    return : body của pape, gồm full cited
            body này đã có info pmid, title, abstract của nhiều paper
            đưa tiếp qua crawl_trending.split_info để lấy thông tin của từng paper

    format của tag html:
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

    # get query string dẫn đến full cited page of paper
    queryStr = show_all_cited.__getitem__(key="data-href")
    full_cited_url = add_query(queryStr)
    cited_body = send_request(full_cited_url)

    return cited_body


if __name__ == "__main__":
    url = r'https://pubmed.ncbi.nlm.nih.gov/32264957/'
    body = send_request(url=url)

    ref_body = find_reference_body(body)
    with open("ref.html", 'w') as f:
        f.write(str(ref_body))

