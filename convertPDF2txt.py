from os.path import isfile, isdir, join, basename
import os
import sys
sys.setrecursionlimit(65535) # 1000
from glob import glob

from pdfminer.high_level import extract_text


def cvtPdf2Txt(folderPDF, folderTXT):
    if not isdir(folderTXT):
        os.makedirs(folderTXT)

    pdfs = glob(folderPDF + '/*.pdf')
    length = len(pdfs)
    for i, pdf in enumerate(pdfs):
        name = basename(pdf)
        name = name.replace('.pdf', '.txt')
        path_txt = join(folderTXT, name)

        # đã convert rồi thì bỏ qua
        if isfile(path_txt):
            continue
        
        try:
            text = extract_text(pdf)
            with open (path_txt, 'w', encoding='utf-8') as f:
                f.write(text)
            print('{:4d}/{}'.format(i, length),name)

        except Exception as e:
            with open('data/cannot_convertpdf.txt', 'a', encoding= 'utf-8') as c:
                c.write(name.strip('.txt') + '\n')
            print('{:4d}/{}'.format(i, length), name, e)

if __name__ == "__main__":
    i = 9
    folderPDF = r'data/fulltext/negative_pdfs/sub{}'.format(i)
    folderTXT = r'data/fulltext/negative_txts/sub{}'.format(i)
    cvtPdf2Txt(folderPDF, folderTXT)
