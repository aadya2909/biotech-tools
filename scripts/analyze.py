from src.mutations.known_mutations import KNOWN_MUTATIONS
import os

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

def analyze_sequence(sequence, gene_id, official_protein=None):
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
    # finalize gene name
    gene_name = gene_id.split('.')[0]

    # choose protein to analyze
    if official_protein:
        protein_to_analyze = official_protein
        protein_source = "Annotated CDS protein"
        print(f"Protein source: {protein_source}")
        print(f"Protein length: {len(protein_to_analyze)} aa")
        print(f"Protein preview: {protein_to_analyze[:80]}")

    elif longest_protein:
        protein_to_analyze = longest_protein
        protein_source = "Longest ORF"
        print(f"Protein source: {protein_source}")
        print(f"Protein length: {len(protein_to_analyze)} aa")
        print(f"Protein preview: {protein_to_analyze[:80]}")

    else:
        print("No valid protein found")
        return {
            "gene": gene_name,
            "sequence_length": len(sequence),
            "protein_length": 0,
            "protein_source": "None",
            "gc_content": round(gc_content, 2),
            "known_sites_checked": 0,
            "mutations_detected": 0,
            "different_variants": 0
        }

    # If we have a protein, check known mutations and save report
    mutation_results = detect_known_mutations(protein_to_analyze, gene_name)
    save_mutation_report(gene_name, protein_to_analyze, mutation_results)

    detected = sum(1 for r in mutation_results if r["status"] == "Mutation detected")
    different = sum(1 for r in mutation_results if r["status"] == "Different variant")

    return {
        "gene": gene_name,
        "sequence_length": len(sequence),
        "protein_length": len(protein_to_analyze),
        "protein_source": protein_source,
        "gc_content": round(gc_content, 2),
        "known_sites_checked": len(mutation_results),
        "mutations_detected": detected,
        "different_variants": different
    }


# ✅ HELPER FUNCTION (OUTSIDE, AT END)
def detect_known_mutations(protein, gene_name):
    print("\n--- Known Mutation Check ---")

    results = []

    if gene_name not in KNOWN_MUTATIONS:
        message = "No mutation data available for this gene"
        print(message)
        return results

    mutations = KNOWN_MUTATIONS[gene_name]

    for m in mutations:
        pos = m["position"]
        expected = m["original"]
        mutated = m["mutated"]

        if len(protein) < pos:
            result = {
                "name": m["name"],
                "position": pos,
                "status": "Protein too short",
                "expected": expected,
                "observed": None,
                "mutated": mutated,
                "type": m["type"],
                "info": m["info"]
            }
            results.append(result)
            continue

        actual = protein[pos - 1]

        if actual == expected:
            status = "Normal"
            print(f"{m['name']}: Normal ({expected} at position {pos})")

        elif actual == mutated:
            status = "Mutation detected"
            print(f"{m['name']}: ⚠️ Mutation detected!")
            print(f"  Change: {expected} → {mutated}")
            print(f"  Type: {m['type']}")
            print(f"  Info: {m['info']}")

        else:
            status = "Different variant"
            print(f"{m['name']}: Different variant ({expected} → {actual})")

        result = {
            "name": m["name"],
            "position": pos,
            "status": status,
            "expected": expected,
            "observed": actual,
            "mutated": mutated,
            "type": m["type"],
            "info": m["info"]
        }

        results.append(result)

    return results

def save_mutation_report(gene_name, protein, mutation_results):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{gene_name}_mutation_report.txt"

    detected = sum(1 for r in mutation_results if r["status"] == "Mutation detected")
    different = sum(1 for r in mutation_results if r["status"] == "Different variant")

    with open(filename, "w") as f:
        f.write("=== Mutation Analysis Report ===\n\n")
        f.write(f"Gene: {gene_name}\n")
        f.write(f"Protein length: {len(protein)} aa\n")
        f.write(f"Known mutation sites checked: {len(mutation_results)}\n\n")

        for r in mutation_results:
            f.write(f"{r['name']}:\n")
            f.write(f"  Position: {r['position']}\n")
            f.write(f"  Expected: {r['expected']}\n")
            f.write(f"  Observed: {r['observed']}\n")
            f.write(f"  Known mutation: {r['mutated']}\n")
            f.write(f"  Status: {r['status']}\n")
            f.write(f"  Type: {r['type']}\n")
            f.write(f"  Info: {r['info']}\n\n")

        f.write("Summary:\n")
        f.write(f"  Known mutations detected: {detected}\n")
        f.write(f"  Different variants found: {different}\n")

    print(f"\nMutation report saved to {filename}")