HOMEPAGE = r"https://pubmed.ncbi.nlm.nih.gov/"

params_cited = {
'show_snippets':'off',
'format':'pubmed',
'size': '200'
}

if __name__ == "__main__":
    from urllib.parse import urljoin, parse_qs, urlencode, urlparse, parse_qsl, urlunparse
    from colorama import Fore
    