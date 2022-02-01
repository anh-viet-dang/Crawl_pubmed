import os
from random import choice
from urllib.parse import parse_qsl, urlencode, urljoin

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .config import PUBMED, params_query


def send_request(url: str) -> Tag:
    r"""
         ____________________________________________________
        |.==================================================,|
        ||  send requests   >>>                             ||
        ||  >>>     receice body of html                    ||
        ||                                                  ||
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

    headers = {'User-Agent': choice(desktop_agents),
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    resp = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    body = soup.find('body')

    return body


def add_query(queryStr:str)->str:
    """
    >>> string query lấy được từ tag html
    >>> return full url để send_request
    """

    # BUG bỏ 2 ký tự '/' và '?' để hàm urlencode hoạt động ok
    queryStr = queryStr.strip('/').strip('?')

    # https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
    # convert query String sang dict
    queryDict = dict(parse_qsl(queryStr))
    # thêm key, value cho queryDict
    queryDict.update(params_query)
    # convert dict sang query string
    queryStr = urlencode(queryDict)
    # BUG thêm 2 ký tự '/' và '?' để hàm urlencode hoạt động ok
    queryStr = '/?' + queryStr
    # BUG ký tự '/' vô hiệu hóa toàn bộ ký tự đặc biệt trong string
    # FIXME s = r''.format(str)

    # join homepage and query string thành url hoàn chỉnh
    full_url = urljoin(PUBMED, queryStr)

    return full_url


def pmid2Url(pmid:str)->str:
    url = r'{}'.format(urljoin(PUBMED, pmid.strip()))
    if url.endswith(r'/'):
        return url
    return url + '/'


def read_pmid(path: str) -> list:
    if not os.path.isfile(path):
        print("ko tìm thấy file pmids")
        return []
    with open(path, 'r') as f:
        list_pmid = f.read().strip().split('\n')
    
    return list(set(list_pmid))


if __name__ == "__main__":
    pmid = '29625052'
    url = pmid2Url(pmid)
    print(url)
