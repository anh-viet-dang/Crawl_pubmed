from typing import overload
from .utils import add_query, pmid2Url, send_request


class ThePaper(object):
    pmid:str
    pmcid:str
    doi:str
    title:str
    abstract:str

    similar:list[tuple[str, str, str]]
    reference:list[tuple[str, str, str]]
    cited:list[tuple[str, str, str]]

    def __init__(self, pmid:str) -> None:
        self.pmid = pmid
    
    @overload
    def __init__(self, pmcid:str) -> None:
        self.pmcid = pmcid
    
    