from src.ncbi.fetch import fetch_gene
from src.ncbi.search import search_gene

gene_name = input("Enter gene name (e.g. TP53): ")

print("Searching for gene...")

gene_id = search_gene(gene_name)

if gene_id:
    print("Found ID:", gene_id)

    record = fetch_gene(gene_id)

    print("\nID:", record.id)
    print("Sequence:", record.seq[:100])

    # 💾 SAVE TO FILE
    filename = f"data/{gene_name}.fasta"
    with open(filename, "w") as f:
        f.write(f">{record.id}\n{record.seq}")

    print(f"\nSaved to {filename}")

else:
    print("Gene not found.")

    # 📊 BASIC ANALYSIS
sequence = record.seq

length = len(sequence)
gc_content = (sequence.count("G") + sequence.count("C")) / length * 100

print("\n--- Analysis ---")
print("Length:", length)
print("GC Content:", round(gc_content, 2), "%")