from lib.pmc import PMC_tree

data_pmc = PMC_tree()
folder_save_pdf = '/home/agent/Documents/AVADA/Pubmed-Batch-Download/fetched_pdfs'

with open("data/pmids.txt", 'r', encoding= 'utf-8') as f:
    pmids = f.read().strip().split('\n')

for pmid in pmids:
    pmid = pmid.strip()
    oa_pdf = data_pmc.find_oa_PDF_from_pmid(pmid)
    if oa_pdf is None:
        print(pmid, "not found")
        with open("data/pmid_not_found_in_pmc_tree.txt", 'a', encoding= 'utf-8') as f:
            f.write(pmid + ',')     # save format này để chuyển qua download = tool bên kia
    else:
        data_pmc.download_PMC(oa_pdf, folder_save_pdf, pmid)
