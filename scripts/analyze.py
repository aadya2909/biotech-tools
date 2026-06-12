from src.mutations.known_mutations import KNOWN_MUTATIONS

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
    for n, count in nucleotide_counts.items():
        print(f"  {n}: {count}")

    # GC content
    gc_content = (nucleotide_counts["G"] + nucleotide_counts["C"]) / len(sequence) * 100
    print(f"GC Content: {gc_content:.2f}%")

    # Start & stop codons
    start_codons = [i for i in range(len(sequence) - 2) if sequence[i:i+3] == "ATG"]

    stop_positions = []
    for stop in ["TAA", "TAG", "TGA"]:
        stop_positions.extend([i for i in range(len(sequence) - 2) if sequence[i:i+3] == stop])

    print(f"Start codons: {len(start_codons)} at positions {start_codons}")
    print(f"Stop codons: {len(stop_positions)} at positions {stop_positions}")

    # ORF detection
    longest_protein = ""

    for i in range(len(sequence) - 2):
        if sequence[i:i+3] == "ATG":
            protein = ""

            for j in range(i, len(sequence), 3):
                codon = sequence[j:j+3]

                if len(codon) < 3:
                    break

                aa = codon_table.get(codon, "?")

                if aa == "*":
                    break

                protein += aa

            if len(protein) > len(longest_protein):
                longest_protein = protein

    # ✅ IMPORTANT: inside function
    if longest_protein:
        print(f"Protein (longest ORF): {longest_protein}")

        # ✅ call helper function here
        detect_known_mutations(longest_protein, gene_id.split('.')[0])

    else:
        print("No valid protein found")


# ✅ HELPER FUNCTION (OUTSIDE, AT END)
def detect_known_mutations(protein, gene_name):
    print("\n--- Known Mutation Check ---")

    if gene_name not in KNOWN_MUTATIONS:
        print("No mutation data available for this gene")
        return

    mutations = KNOWN_MUTATIONS[gene_name]

    for m in mutations:
        pos = m["position"]
        expected = m["original"]
        mutated = m["mutated"]

        if len(protein) < pos:
            continue

        actual = protein[pos - 1]  # biology → python index

        if actual == expected:
            print(f"{m['name']}: Normal ({expected} at position {pos})")

        elif actual == mutated:
            print(f"{m['name']}: ⚠️ Mutation detected!")
            print(f"  Change: {expected} → {mutated}")
            print(f"  Type: {m['type']}")
            print(f"  Info: {m['info']}")

        else:
            print(f"{m['name']}: Different variant ({expected} → {actual})")