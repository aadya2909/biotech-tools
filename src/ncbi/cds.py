from Bio import Entrez, SeqIO
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

Entrez.email = "pachputeaadya888@gmail.com"


def fetch_genbank_record(id_list):
    print("Fetching GenBank record from NCBI...")

    for gene_id in id_list:
        print(f"Trying GenBank ID: {gene_id}")

        handle = Entrez.efetch(
            db="nucleotide",
            id=gene_id,
            rettype="gb",
            retmode="text"
        )

        record = SeqIO.read(handle, "genbank")
        handle.close()

        if record.id.startswith("NM_"):
            print("Selected GenBank RefSeq:", record.id)
            return record

    print("No valid NM_ GenBank record found.")
    return None


def extract_cds_info(record):
    for feature in record.features:
        if feature.type == "CDS":
            cds_sequence = feature.extract(record.seq)

            protein = feature.qualifiers.get("translation", [None])[0]
            gene = feature.qualifiers.get("gene", ["Unknown"])[0]
            product = feature.qualifiers.get("product", ["Unknown"])[0]

            return {
                "gene": gene,
                "product": product,
                "cds_sequence": str(cds_sequence),
                "protein": protein,
                "protein_length": len(protein) if protein else 0
            }

    return None