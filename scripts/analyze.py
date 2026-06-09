codon_table = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}


from Bio import SeqIO

record = SeqIO.read("data/TP53.fasta", "fasta")
sequence = str(record.seq).upper()

print("Gene:", record.id)
print("Length:", len(sequence), "bp")

# Count nucleotides
nucleotide_counts = {"A": sequence.count("A"),
                     "T": sequence.count("T"),
                     "G": sequence.count("G"),
                     "C": sequence.count("C")}

print("Nucleotide counts:")
for nucleotide, count in nucleotide_counts.items():
    print(f"{nucleotide}: {count}")

# Calculate GC content
gc_content = (nucleotide_counts["G"] + nucleotide_counts["C"]) / len(sequence) * 100
print(f"GC Content: {gc_content:.2f}%")

# Codon analysis 
codons = [sequence[i:i+3] for i in range(0, len(sequence) - 2, 3)]
print(f"Total codons: {len(codons)}")
print("Codons:")
for codon in codons:
    print(codon)

# Find start codons (ATG)
start_codons = [i for i in range(len(sequence) - 2) if sequence[i:i+3] == "ATG"]
print(f"Start codons found: {len(start_codons)} at positions: {start_codons}")

# Find stop codons 
stop_codons = ["TAA", "TAG", "TGA"]
stop_codon_positions = []
for stop_codon in stop_codons:
    positions = [i for i in range(len(sequence) - 2) if sequence[i:i+3] == stop_codon]
    stop_codon_positions.extend(positions)
print(f"Stop codons found: {len(stop_codon_positions)} at positions: {stop_codon_positions}") 


protein = ""
for i in range(0, len(sequence), 3):
    codon = sequence[i:i+3]
    if len(codon) == 3:
        amino_acid =  codon_table.get(codon, '?')
        protein = protein + amino_acid

print("Protein:", protein)