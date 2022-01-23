# Crawl_pubmed


## mô tả bug

file crawl_trending.py  def get_from_format_pubmed line 90, 
nếu k có .strip() sẽ ko print đc dòng 154 biến paper[0] 
nguyên nhân:    https://www.tutorialsteacher.com/python/string-isprintable#:~:text=Non%2Dprintable%20characters%20are%20characters,come%20under%20Non%2DPrintable%20characters