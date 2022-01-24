def read_pmid(path: str) -> list:
    with open(path, 'r') as f:
        list_pmid = f.read().strip().split('\n')
    
    return list_pmid