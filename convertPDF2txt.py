import os
from glob import glob

from pdfminer.high_level import extract_text

folderPDF = r'data/fetched_pdfs'
folderTXT = r'data/fetched_txts'

pdfs = glob(folderPDF + '/*.pdf')
txts = glob(folderTXT + '/*.txt')
for pdf in pdfs:
    name = os.path.basename(pdf)
    name = name.replace('.pdf', '.txt')
    path_txt = os.path.join(folderTXT, name)

    # đã convert rồi thì bỏ qua
    if os.path.isfile(path_txt):
        continue

    try:
        text = extract_text(pdf)
        with open (path_txt, 'w') as f:
            f.write(text)
        print(name)

    except Exception as e:
        with open('data/cannot_convertpdf.txt', 'a') as c:
            c.write(name.strip('.txt') + '\n')
        print(name, e)
