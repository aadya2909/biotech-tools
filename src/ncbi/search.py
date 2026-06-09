from Bio import Entrez

Entrez.email = "your_real_email@gmail.com"

def search_gene(gene_name):
    handle = Entrez.esearch(
        db="nucleotide",
        term=f"{gene_name}[Gene] AND Homo sapiens[Organism] AND mRNA[Filter]",
        retmax=1
    )

    record = Entrez.read(handle)
    handle.close()

    if record["IdList"]:
        return record["IdList"][0]
    else:
        return None