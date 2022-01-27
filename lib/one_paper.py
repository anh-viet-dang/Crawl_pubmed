from urllib.parse import urljoin

from bs4.element import Tag

from .config import PUBMED
from .utils import add_query, send_request


def find_DOI(body:Tag) -> str:
    r"""
                <li>
              <span class="identifier doi">
                <span class="id-label"> DOI: </span>
                <a
                  class="id-link"
                  data-ga-action="DOI"
                  data-ga-category="full_text"
                  href="https://doi.org/10.1016/0165-0270(89)90131-3"
                  ref="linksrc=article_id_link&amp;article_id=10.1016/0165-0270(89)90131-3&amp;id_type=DOI"
                  rel="noopener"
                  target="_blank"
                >
                  10.1016/0165-0270(89)90131-3
                </a>
              </span>
            </li>
    """
    doi_Tag = body.find("a", attrs= {"class":"id-link",
                                    "data-ga-action":"DOI",
                                    "data-ga-category":"full_text",
                                    "rel":"noopener",
                                    "target":"_blank"
                                    }, recursive=True)
    if doi_Tag is None:
        return ""
    else:
        return doi_Tag.get_text(strip=True).strip()


def find_PMC(body:Tag) -> str:
    r"""
                <li>
              <span class="identifier pmc">
                <span class="id-label"> PMCID: </span>
                <a
                  class="id-link"
                  data-ga-action="PMCID"
                  data-ga-category="full_text"
                  href="http://www.ncbi.nlm.nih.gov/pmc/articles/pmc1435730/"
                  ref="linksrc=article_id_link&amp;article_id=PMC1435730&amp;id_type=PMC"
                  rel="noopener"
                  target="_blank"
                >
                  PMC1435730
                </a>
              </span>
            </li>
    """
    pmcid_tag = body.find('a', attrs={"class":"id-link",
                                    "data-ga-action":"PMCID",
                                    "data-ga-category":"full_text",
                                    "rel":"noopener",
                                    "target":"_blank"
                                    }, recursive= True)
    if pmcid_tag is None:
        return ""       # paper không có pmcid
    else:
        return pmcid_tag.get_text(strip= True).strip()


def find_title(body: Tag) -> str:
    # get title of paper
    title = body.find(name='h1', attrs={"class": "heading-title"})
    title =  title.get_text(strip= True).strip()
    return ' '.join(title.split())


def find_abstract(body: Tag) -> str:
    # get abstrack of paper
    absTag = body.find(name='div', attrs={"class": "abstract"}, recursive=True)
    if absTag is None:
        # tìm sai keywork trong tag html
        # nên ko tìm đc Tag chứa abstract
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
            abstract = ' '.join(abstract.split()) # loại bỏ các dấu xuống dòng, nhiều space về 1 space
    return abstract


def find_reference_body(body: Tag) -> Tag:
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

    if show_all_ref is None:
        return None  # nếu ko tìm thấy tag, return None
    
    nextPageUrl = show_all_ref.__getitem__(key="data-next-page-url")    # "/32264957/references/"

    # ref paper KO theo format nên ko dùng func add_query
    full_ref_url = urljoin(PUBMED, nextPageUrl)
    ref_body = send_request(full_ref_url)


    # <ol class="references-list" id="full-references-list-1">
    # ol = ref_body.find('ol', {"class":"references-list"}, recursive= True)

    return ref_body


def find_similar_body(body: Tag)->Tag:
    """
        5 url to 5 similar articals and 1 to search 1901 similar articals
    """
    see_allSimilarTag = body.find('a', {"class": "usa-button show-all-linked-articles", 
                                             "data-ga-action": "show_all", 
                                             "data-ga-category": "similar_article"}, recursive=True)
    if see_allSimilarTag is None:
        return None
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
