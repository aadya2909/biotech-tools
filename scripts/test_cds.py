from src.ncbi.search import search_gene
from src.ncbi.cds import fetch_genbank_record, extract_cds_info


def main():
    gene_name = "TP53"

    id_list = search_gene(gene_name)
    print("Found IDs:", id_list)

    record = fetch_genbank_record(id_list)

    if not record:
        print("No GenBank record found.")
        return

    cds_info = extract_cds_info(record)

    if not cds_info:
        print("No CDS found.")
        return

    print("\n--- CDS Info ---")
    print("Gene:", cds_info["gene"])
    print("Product:", cds_info["product"])
    print("CDS length:", len(cds_info["cds_sequence"]))
    print("Protein length:", cds_info["protein_length"])
    print("Protein preview:", cds_info["protein"][:80])


if __name__ == "__main__":
    main()