import requests
from .config import SCIHUB
doi = r'10.1016/j.semcancer.2020.02.016'


def download_scihub(doi:str) -> int:
    resp = requests.get(SCIHUB + doi.strip())
    if resp.status_code == 200:
        with open ('32112814.pdf', 'wb') as f:
            f.write(resp.content)
    return resp.status_code