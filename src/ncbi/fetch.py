from Bio import Entrez, SeqIO
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

Entrez.email = "pachputeaadya888@gmail.com"

def fetch_gene(id_list):
    print("Fetching from NCBI...")

    for gene_id in id_list:
        print(f"Trying ID: {gene_id}")

        handle = Entrez.efetch(
            db="nucleotide",
            id=gene_id,
            rettype="fasta",
            retmode="text"
        )

        record = SeqIO.read(handle, "fasta")
        handle.close()

        # 🔥 FILTER: only accept NM_ (RefSeq mRNA)
        if record.id.startswith("NM_"):
            print("Selected RefSeq:", record.id)
            return record

    print("No valid NM_ sequence found.")
    return None