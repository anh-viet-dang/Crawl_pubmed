## pmid_gene.txt chứa pmid của các paper có lien quan đến gene
Tạm thời để xác định các pmid này, lấy thủ công các file html từ hgmd, từ đó lấy ra pmid
## pmid_not_gene.txt chứa pmid của các paper ko liên quan đến gen
crawl random từ pubmed
## folder paper chứa các file có format

### tên file : pmid + .txt

### nội dung:

- line 1 : pmid
- line 2 : title
- line 3 : abstract
- line 3 có thể ko có nội dung , do 1 số lượng paper ko có abstract
- line 4: '\n' để ngăn cách giữa 2 paper với nhau

### Các nguồn để crawl paper
- HGMD -> pmid -> pubmed
- pubmed -> pmid
- PMC -> title -> search in pubmed



Pmid_title_abstract.txt là thông tin về các pmid lấy được từ HGMD
similar1.txt            là thông tin pmid lấy được từ các pmid là similar với các pmid trong Pmid_title_abstract
pmid_not_gene.txt là các pmid của các paper ko liên quan đến bệnh di truyền