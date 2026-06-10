from Bio import Entrez

# Always set your email (NCBI requirement)
Entrez.email = "pachputeaadya888@gmail.com"


def search_gene(gene_name):
    print("Searching for gene...")

    handle = Entrez.esearch(
        db="nucleotide",
        term=f"{gene_name}[Gene] AND Homo sapiens[Organism] AND mRNA[Filter]",
        retmax=20   # 🔥 important: get multiple results
    )

    record = Entrez.read(handle)
    handle.close()

    id_list = record.get("IdList", [])

    if not id_list:
        print("No IDs found.")
        return []

    return id_list