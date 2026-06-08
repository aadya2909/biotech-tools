codon_table = {
    'TTT': 'Phe', 'TTC': 'Phe', 'TTA': 'Leu', 'TTG': 'Leu',
    'CTT': 'Leu', 'CTC': 'Leu', 'CTA': 'Leu', 'CTG': 'Leu',
    'ATT': 'Ile', 'ATC': 'Ile', 'ATA': 'Ile', 'ATG': 'Met',
    'GTT': 'Val', 'GTC': 'Val', 'GTA': 'Val', 'GTG': 'Val',
    'TCT': 'Ser', 'TCC': 'Ser', 'TCA': 'Ser', 'TCG': 'Ser',
    'CCT': 'Pro', 'CCC': 'Pro', 'CCA': 'Pro', 'CCG': 'Pro',
    'ACT': 'Thr', 'ACC': 'Thr', 'ACA': 'Thr', 'ACG': 'Thr',
    'GCT': 'Ala', 'GCC': 'Ala', 'GCA': 'Ala', 'GCG': 'Ala',
    'TAT': 'Tyr', 'TAC': 'Tyr', 'TAA': 'Stop', 'TAG': 'Stop',
    'CAT': 'His', 'CAC': 'His', 'CAA': 'Gln', 'CAG': 'Gln',
    'AAT': 'Asn', 'AAC': 'Asn', 'AAA': 'Lys', 'AAG': 'Lys',
    'GAT': 'Asp', 'GAC': 'Asp', 'GAA': 'Glu', 'GAG': 'Glu',
    'TGT': 'Cys', 'TGC': 'Cys', 'TGA': 'Stop', 'TGG': 'Trp',
    'CGT': 'Arg', 'CGC': 'Arg', 'CGA': 'Arg', 'CGG': 'Arg',
    'AGT': 'Ser', 'AGC': 'Ser', 'AGA': 'Arg', 'AGG': 'Arg',
    'GGT': 'Gly', 'GGC': 'Gly', 'GGA': 'Gly', 'GGG': 'Gly',
}


reference = "ATGACTGAATATAAACTTGTGGTAGTTGGAGCTGGTGGCGTAGGCAAGAGT".upper()
patient   = "ATGACTGAATATAAACTTGTGGTAGTTGGAGCTGATGGCGTAGGCAAGAGT".upper()

gc_count = reference.count("G") + reference.count("C")
gc_content = round((gc_count / len(reference)) * 100, 2)
print("GC content:", gc_content, "%")
if gc_content > 60:
    print("Classification: GC-rich region (possibly promoter or CpG island)")
elif gc_content >= 40:
    print("Classification: Normal GC range (typical coding region)")
else:
    print("Classification: AT-rich region (possibly regulatory or repeat region)")

print("\n--- Base-by-base scan ---")
for base in reference:
    print(base, end="")
print()

print("\n--- Position tracking ---")
for index, base in enumerate(reference):
    if index < 3:
        print(f"Position {index}: {base}")

print("\n--- Codon scan ---")
codon_number = 1
for i in range(0, len(reference), 3):
    codon = reference[i:i+3]
    if len(codon) == 3:
        print(f"Codon {codon_number}: {codon}")
        codon_number += 1

print("\n--- Mutation detection ---")
if len(reference) != len(patient):
    print("Sequences are different lengths — cannot compare directly.")
else:
    mutations_found = 0
    for i in range(len(reference)):
        if reference[i] != patient[i]:
            print(f"Mutation at position {i}: {reference[i]} → {patient[i]}")
            codon_number = (i // 3) + 1
            codon_start = (i // 3) * 3
            codon_ref = reference[codon_start : codon_start + 3]
            codon_pat = patient[codon_start : codon_start + 3]
            print(f"  → Codon {codon_number}: {codon_ref} (ref) changed to {codon_pat} (patient)")
            aa_ref = codon_table.get(codon_ref, '?')
            aa_pat = codon_table.get(codon_pat, '?')
            print(f"  → Amino acid change: {aa_ref} → {aa_pat}")
            
            mutations_found += 1


    print(f"\nTotal mutations found: {mutations_found}")
    if mutations_found == 0:
        print("Classification: No mutation")
    elif mutations_found == 1:
        print("Classification: Single mutation — possible SNP")
    else:
        print("Classification: Multiple mutations — review required")



print("\n--- All ATG positions ---")
motif = "ATG"
positions = []
for i in range(len(reference) - len(motif) + 1):
    if reference[i:i+len(motif)] == motif:
        positions.append(i)
if positions:
    print(f"'{motif}' found at positions: {positions}")
else:
    print(f"'{motif}' not found.")

# Clinical interpretation
KRAS_KNOWN = {
    'G12D': ('GGT', 'GAT', 12),
    'G12V': ('GGT', 'GTT', 12),
    'G12C': ('GGT', 'TGT', 12),
}

print("\n--- Clinical interpretation ---")
match_found = False
for mutation_name, (ref_codon, mut_codon, codon_pos) in KRAS_KNOWN.items():
    for i in range(len(reference)):
        if reference[i] != patient[i]:
            cs = (i // 3) * 3
            cn = (i // 3) + 1
            if cn == codon_pos and reference[cs:cs+3] == ref_codon and patient[cs:cs+3] == mut_codon:
                print(f"  ⚠ Known oncogenic mutation detected: KRAS {mutation_name}")
                print(f"  Found in ~36% of pancreatic cancers, ~40% of colorectal cancers")
                match_found = True
if not match_found:
    print("  No known KRAS hotspot mutations detected in this fragment")
    