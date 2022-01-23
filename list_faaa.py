folder = "/home/agent/Documents/AVADA/Pubmed-Batch-Download/fetched_pdfs"

import os
from glob import glob

x = glob(folder + '/*.pdf')
print(len(x))
y = glob(folder + '/*.html')
print(len(y))