from Bio import Entrez, SeqIO
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

Entrez.email = "pachputeaadya888@gmail.com"

def fetch_gene(gene_id):
    print("Fetching from NCBI...")

    handle = Entrez.efetch(
        db="nucleotide",
        id=gene_id,
        rettype="fasta",
        retmode="text"
    )

    record = SeqIO.read(handle, "fasta")
    handle.close()

    return record