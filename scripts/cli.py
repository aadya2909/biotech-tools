import argparse
import csv
import os

from src.ncbi.fetch import fetch_gene
from src.ncbi.search import search_gene
from src.ncbi.cds import fetch_genbank_record, extract_cds_info
from scripts import analyze

def save_summary_csv(summaries):
    os.makedirs("reports", exist_ok=True)

    filename = "reports/mutation_summary.csv"

    fieldnames = [
    "gene",
    "sequence_length",
    "protein_length",
    "protein_source",
    "gc_content",
    "known_sites_checked",
    "mutations_detected",
    "different_variants"
]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"\nCSV summary saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Gene Fetch Tool")

    # Single gene
    parser.add_argument(
        "--gene",
        type=str,
        required=False,
        help="Gene name (e.g. TP53, BRCA1, KRAS)"
    )

    # Multiple genes
    parser.add_argument(
        "--genes",
        nargs="+",
        type=str,
        help="List of genes (e.g. TP53 KRAS BRCA1)"
    )

    args = parser.parse_args()

    # Decide input type
    if args.genes:
        gene_list = args.genes
    elif args.gene:
        gene_list = [args.gene]
    else:
        print("Please provide --gene or --genes")
        return

    summaries = []
    
    # Process each gene
    for gene_name in gene_list:
        print(f"\nSearching for {gene_name}...")

        id_list = search_gene(gene_name)
        print("Found IDs:", id_list)

        record = fetch_gene(id_list)

        # ✅ SAFE handling
        if record:
            print("\nID:", record.id)
            print("Sequence:", record.seq[:100])

            # Save file
            filename = f"data/{gene_name}.fasta"
            with open(filename, "w") as f:
                f.write(f">{record.id}\n{record.seq}")

            print(f"Saved to {filename}")

            # Analyze
            official_protein = None
            # Try to get annotated CDS protein from GenBank
            genbank_record = fetch_genbank_record(id_list)

            if genbank_record:
                cds_info = extract_cds_info(genbank_record)

                if cds_info and cds_info.get("protein"):
                    official_protein = cds_info["protein"]
                    print("\nUsing annotated CDS protein for mutation analysis.")
                else:
                    print("\nNo CDS protein found. Falling back to longest ORF.")

            summary = analyze.analyze_sequence(
                str(record.seq),
                gene_name,
                official_protein=official_protein
            )

            if summary:
                summaries.append(summary)
            else:
                print("No valid sequence found.")

    # End for gene_list

    if summaries:
        save_summary_csv(summaries)

if __name__ == "__main__":
    main()
