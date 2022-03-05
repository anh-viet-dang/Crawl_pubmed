from os.path import isfile, isdir, join, basename
import os
import sys
sys.setrecursionlimit(32000) # 1000
from glob import glob

from pdfminer.high_level import extract_text


def cvtPdf2Txt(folderPDF, folderTXT):
    if not isdir(folderTXT):
        os.makedirs(folderTXT)

    pdfs = glob(folderPDF + '/*.pdf')
    for pdf in pdfs:
        name = basename(pdf)
        pmid_index = name.strip('.pdf')
        name = name.replace('.pdf', '.txt')
        path_txt = join(folderTXT, name)

        # đã convert rồi thì bỏ qua
        if isfile(path_txt):
            continue

        try:
            text = extract_text(pdf)
            with open (path_txt, 'w', encoding='utf-8') as f:
                f.write(text)
            print(pmid_index)

        except Exception as e:
            with open('data/cannot_convertpdf.txt', 'a', encoding= 'utf-8') as c:
                c.write(pmid_index + '\n')
            print(pmid_index, e)

if __name__ == "__main__":
    folderPDF = r'data/fulltext/similar_pdfs/similar_1'
    folderTXT = r'data/fulltext/similar_txts/similar_1'
    
    cvtPdf2Txt(folderPDF, folderTXT)
