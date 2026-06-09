dna_sequence = "ATGGAGGAGCCGCAGTCAGATCCTAGCGTTGAATGAGCCCTGGAACTT"
gene_name = "P53_fragment"

dna_clean = dna_sequence.upper()
sequence_length = len(dna_clean)
print("Gene:", gene_name)
print("Sequence:", dna_clean)
print("Length:", sequence_length, "base pairs")

count_A = dna_clean.count("A")
count_T = dna_clean.count("T")
count_G = dna_clean.count("G")
count_C = dna_clean.count("C")
print("\nNucleotide counts:")
print("A:", count_A)
print("T:", count_T)
print("G:", count_G)
print("C:", count_C)

gc_count = count_G + count_C
gc_content = round((gc_count / sequence_length) * 100, 2)
print("\nGC content:", gc_content, "%")

start_codon = "ATG"
position = dna_clean.find(start_codon)
if position != -1:
    print("\nStart codon found at position:", position)
else:
    print("\nNo start codon found.")

first_three_codons = dna_clean[0:9]
print("First 3 codons:", first_three_codons)

result = f"Gene: {gene_name} | Length: {sequence_length} bp | GC: {gc_content}%"
print("\nFormatted result:")
print(result)  