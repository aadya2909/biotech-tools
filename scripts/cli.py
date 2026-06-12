import argparse
from src.ncbi.fetch import fetch_gene
from src.ncbi.search import search_gene
from scripts import analyze


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
            analyze.analyze_sequence(str(record.seq), gene_name)

        else:
            print("No valid sequence found.")


if __name__ == "__main__":
    main()
