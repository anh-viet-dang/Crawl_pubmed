from lib.pmc import PMC_tree

data_pmc = PMC_tree()

with open("data/pmids.txt", 'r', encoding= 'utf-8') as f:
    pmids = f.read().strip().split('\n')

for pmid in pmids:
    oa_pdf = data_pmc.find_oa_PDF_from_pmid(pmid.strip())
    if oa_pdf is None:
        print(pmid, "not found")
        with open("pmid_not_found_in_pmc_tree.txt", 'a', encoding= 'utf-8') as f:
            f.write(pmid + '\n')
    else:
        data_pmc.download_PMC(oa_pdf, 'data/full_text_pdf')