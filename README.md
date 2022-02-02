# Crawl_pubmed

## TODO
1. crawl negative
2. random forest
3. logistic regression
4. SVM
5. Naive Bayes Classifier
### FTH
`https://ftp.ncbi.nlm.nih.gov/pub/pmc/`


# Pubmed-Batch-Download

Version 3.0.0  Last update: 9/15/2020.

```
python fetch_pdfs.py [-pmids or -pmf] [optional arguments]
```

**Example script usage:**

```
python fetch_pdfs.py -pmids 123,124,125,23923,111
```

`https://stackoverflow.com/questions/37804479/how-to-download-full-article-text-from-pubmed
https://github.com/billgreenwald/Pubmed-Batch-Download`


#TODO
zip folder data , cho len colab
chạy python negative_pubmed.py

trong lúc craw, 1 tiếng dừng 1 lần để xem đc bn pmid, ~100k là dừng
làm sk learn để classify text, dùng logistic regression
