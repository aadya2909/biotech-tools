# biotech-tools

Python scripts for biological sequence analysis.
Built as part of my self-directed learning in computational biology.

## Scripts

### p53_analyzer.py
Analyzes a p53 tumor suppressor gene fragment.
- Calculates GC content
- Counts nucleotides
- Detects start codon position
- Scans first 3 codons


### kras_analyzer.py

KRAS is one of the most frequently mutated oncogenes in human cancer. 
This script compares a reference KRAS sequence against a patient sequence 
to identify mutations at the nucleotide, codon, and amino acid level.

**What it does:**
- Detects single nucleotide variants (SNVs) with exact position tracking
- Calculates affected codon and translates to amino acid change
- Flags known oncogenic hotspot mutations: G12D, G12V, G12C
- Provides clinical context — KRAS G12D is present in ~36% of 
  pancreatic cancers and ~40% of colorectal cancers

**Why it matters:**
KRAS mutations are a major focus of targeted cancer therapy research. 
Identifying which specific mutation is present directly influences 
treatment decisions in clinical oncology.

**Test sequences:** Based on the KRAS oncogene (codons 1–17 fragment).

## Author
Aadya | Biotechnology student | Building at the intersection of biology and code