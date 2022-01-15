from urllib import response
from crawl_trending import send_request
from bs4 import BeautifulSoup


url1 = 'https://pubmed.ncbi.nlm.nih.gov/32436578/'  # fully             32436578
url2 = 'https://pubmed.ncbi.nlm.nih.gov/32745377/'  # short abstract    7
url3 = 'https://pubmed.ncbi.nlm.nih.gov/32373318/'  # covid in VN       318 no abstract


response1 = send_request(url= url3)
soup = BeautifulSoup(response1.text, "lxml")
body = soup.find('body')

# with open("32373318.html", 'w') as f:
#     f.write(str(body))