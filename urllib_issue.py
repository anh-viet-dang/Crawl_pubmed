# /home/agent/anaconda3/bin/python3.9
# python version 3.9.7

from urllib.parse import urlencode, parse_qsl

query_string = "/?linkname=pubmed_pubmed_citedin&amp;from_uid=32264957"
queryDict = dict(parse_qsl(query_string))
print(queryDict)
queryStr = urlencode(queryDict)
print(queryStr)
# full_cited_url = urljoin(HOMEPAGE, queryStr)