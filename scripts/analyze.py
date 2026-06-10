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

def analyze_sequence(sequence, gene_id):
    sequence = sequence.upper()

    print(f"\n--- Full Analysis: {gene_id} ---")
    print(f"Length: {len(sequence)} bp")

    # Nucleotide counts
    nucleotide_counts = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C")
    }
    print("Nucleotide counts:")
    for nucleotide, count in nucleotide_counts.items():
        print(f"  {nucleotide}: {count}")

    # GC content
    gc_content = (nucleotide_counts["G"] + nucleotide_counts["C"]) / len(sequence) * 100
    print(f"GC Content: {gc_content:.2f}%")

    # Start and stop codons
    start_codons = [i for i in range(len(sequence) - 2) if sequence[i:i+3] == "ATG"]
    stop_codon_positions = []
    for stop in ["TAA", "TAG", "TGA"]:
        stop_codon_positions.extend([i for i in range(len(sequence) - 2) if sequence[i:i+3] == stop])
    print(f"Start codons: {len(start_codons)} at positions {start_codons}")
    print(f"Stop codons: {len(stop_codon_positions)} at positions {stop_codon_positions}")

    # Protein translation (find longest ORF)
    longest_protein = ""
    for i in range(len(sequence) - 2):
        if sequence[i:i+3] == "ATG":
            protein = ""

            for j in range(i, len(sequence), 3):
                codon = sequence[j:j+3]

                if len(codon) < 3:
                    break

                amino_acid = codon_table.get(codon, '?')

                if amino_acid == "*":
                    break

                protein += amino_acid

            # keep longest protein
            if len(protein) > len(longest_protein):
                longest_protein = protein

    if longest_protein:
        print(f"Protein (longest ORF): {longest_protein}")
    else:
        print("No valid protein found")