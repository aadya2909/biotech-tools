import argparse
from src.ncbi.fetch import fetch_gene
from src.ncbi.search import search_gene
from scripts import analyze

def main():
    parser = argparse.ArgumentParser(description="Gene Fetch Tool")

    parser.add_argument(
        "--gene",
        type=str,
        required=True,
        help="Gene name (e.g. TP53, BRCA1, KRAS)"
    )

    args = parser.parse_args()
    gene_name = args.gene

    print(f"Searching for {gene_name}...")

    gene_id = search_gene(gene_name)

    if gene_id:
        print("Found ID:", gene_id)

        record = fetch_gene(gene_id)

        print("\nID:", record.id)
        print("Sequence:", record.seq[:100])

        # Save file
        filename = f"data/{gene_name}.fasta"
        with open(filename, "w") as f:
            f.write(f">{record.id}\n{record.seq}")

        print(f"\nSaved to {filename}")

        analyze.analyze_sequence(str(record.seq), record.id)

    else:
        print("Gene not found.")

if __name__ == "__main__":
    main()