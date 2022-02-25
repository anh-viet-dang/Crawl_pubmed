import requests

from .config import SCIHUB, PMID2DOI_FILE_PATH
from .one_paper import find_DOI
from .utils import pmid2Url, send_request

# doi = r'10.1016/j.semcancer.2020.02.016'




class Scihub:
    @staticmethod
    def pmid2doi(pmid:str, is_save:bool = True, path_save:str= PMID2DOI_FILE_PATH) -> str:
        """
        sent request to pubmed để tìm doi
        """
        full_url = pmid2Url(pmid)
        body = send_request(full_url)
        doi = find_DOI(body)
        if is_save:
            with open(path_save, 'a', encoding= 'utf-8') as f:
                f.write(pmid + ',' + doi + '\n')
        return doi

    @staticmethod
    def download_scihub(doi:str, path_save:str) -> int:
        """
        input doi:str
        return status_code của respones
        save pdf nếu = 200
        """
        if doi == '':
            return None

        resp = requests.get(SCIHUB + doi.strip())
        if resp.status_code == 200:
            with open (path_save, 'wb') as f:
                f.write(resp.content)
        return resp.status_code
