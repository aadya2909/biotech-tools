# biotech-tools

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Bioinformatics](https://img.shields.io/badge/Field-Bioinformatics-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)


A Python-based bioinformatics pipeline for retrieving gene sequences from NCBI, analyzing nucleotide composition, extracting annotated CDS proteins, and generating mutation analysis reports.

## Overview

`biotech-tools` is a beginner-friendly computational biology project built to explore how real biological sequence data can be accessed, processed, and analyzed using Python.

Starting from a gene name such as `TP53`, `KRAS`, or `BRCA1`, the pipeline searches NCBI, retrieves RefSeq mRNA records, performs sequence-level analysis, extracts annotated CDS protein information from GenBank records, and generates structured output files for downstream interpretation.

The project is educational and research-oriented. It is not intended for clinical diagnosis, treatment decisions, or medical interpretation.

## Features

* Gene search using the NCBI Entrez API
* RefSeq mRNA filtering for `NM_` accessions
* FASTA sequence retrieval and export
* Nucleotide composition analysis
* GC content calculation
* Start and stop codon detection
* Longest open reading frame detection
* GenBank record retrieval
* Annotated CDS extraction
* Official protein sequence extraction from GenBank CDS features
* Known mutation site checking using a small curated mutation database
* Text-based mutation report generation
* CSV summary export for multiple genes
* CLI support for single-gene and multi-gene workflows
* GC content visualization across selected cancer-associated genes

## Why CDS extraction matters

Earlier versions of this project used the longest ORF as a proxy for protein translation. This is useful for learning, but it can produce incorrect protein coordinates for mutation analysis.

The current version improves this by extracting the annotated CDS protein from GenBank records when available.

This allows mutation positions such as TP53 R175H or R248Q to be checked against the correct annotated protein sequence instead of a guessed longest ORF.

Current logic:

```text
Gene name
→ NCBI search
→ RefSeq mRNA selection
→ FASTA sequence analysis
→ GenBank CDS extraction
→ Annotated protein sequence
→ Mutation report
→ CSV summary
```

## Project structure

```text
biotech-tools/
├── data/
│   ├── BRCA1.fasta
│   ├── KRAS.fasta
│   ├── TP53.fasta
│   └── gc_content_comparison.png
│
├── reports/
│   ├── TP53_mutation_report.txt
│   ├── KRAS_mutation_report.txt
│   ├── BRCA1_mutation_report.txt
│   └── mutation_summary.csv
│
├── scripts/
│   ├── cli.py
│   ├── analyze.py
│   ├── fetch_gene.py
│   ├── test_cds.py
│   ├── visualize.py
│   ├── p53_analyzer.py
│   └── kras_analyzer.py
│
├── src/
│   ├── ncbi/
│   │   ├── fetch.py
│   │   ├── search.py
│   │   └── cds.py
│   │
│   └── mutations/
│       └── known_mutations.py
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/aadya2909/biotech-tools.git
cd biotech-tools
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Main dependencies:

```text
biopython
matplotlib
```

## Usage

### Analyze a single gene

```bash
python -m scripts.cli --gene TP53
```

### Analyze multiple genes

```bash
python -m scripts.cli --genes TP53 KRAS BRCA1
```

The pipeline will:

1. Search for the gene in NCBI
2. Fetch a RefSeq mRNA FASTA record
3. Save the sequence to the `data/` directory
4. Perform nucleotide and GC content analysis
5. Retrieve the GenBank record
6. Extract annotated CDS protein information
7. Run known mutation site checks
8. Generate text reports
9. Generate a CSV summary file

## Example terminal output

```text
Searching for TP53...
Selected RefSeq: NM_001407264.1

Length: 2522 bp
GC Content: 52.78%

Using annotated CDS protein for mutation analysis.
Protein source: Annotated CDS protein
Protein length: 393 aa

--- Known Mutation Check ---
R175H: Normal (R at position 175)
R248Q: Normal (R at position 248)

Mutation report saved to reports/TP53_mutation_report.txt
CSV summary saved to reports/mutation_summary.csv
```

## Example CSV output

```csv
gene,sequence_length,protein_length,protein_source,gc_content,known_sites_checked,mutations_detected,different_variants
TP53,2522,393,Annotated CDS protein,52.78,2,0,0
```

## Mutation reports

For supported genes, the pipeline creates a text report in the `reports/` directory.

Example:

```text
=== Mutation Analysis Report ===

Gene: TP53
Protein length: 393 aa
Known mutation sites checked: 2

R175H:
  Position: 175
  Expected: R
  Observed: R
  Known mutation: H
  Status: Normal
  Type: Missense
  Info: Common tumor suppressor mutation

Summary:
  Known mutations detected: 0
  Different variants found: 0
```

## Visualization

![GC content comparison across cancer-associated genes](./data/gc_content_comparison.png)

The project includes a visualization script for comparing GC content across selected cancer-associated genes.


Run:

```bash
python -m scripts.visualize
```

Output:

```text
data/gc_content_comparison.png
```

## Current mutation database

The mutation database is intentionally small and educational. It currently includes selected known mutation sites for genes such as:

* TP53
* KRAS

The database is stored in:

```text
src/mutations/known_mutations.py
```

This can be expanded in future versions with more genes, mutation annotations, and external references.

## Limitations

This project is not a clinical tool.

Important limitations:

* Mutation checking is based on a small manually defined mutation database.
* The tool does not analyze patient sequencing data.
* It does not detect novel mutations from raw sequencing files.
* It does not perform variant calling.
* It does not provide diagnosis, prognosis, or treatment guidance.
* Biological interpretation is simplified for learning purposes.

The project is intended for education, portfolio development, and practical learning in bioinformatics.


## What I learned

This project helped me practice:

* Python programming
* Working with biological sequence data
* Using Biopython and NCBI Entrez
* Understanding FASTA and GenBank formats
* RefSeq accession filtering
* GC content analysis
* ORF detection
* CDS extraction
* Protein translation concepts
* Basic mutation annotation
* CLI tool development
* File handling and CSV export
* Git and GitHub project management

## Author

Aadya
BSc Biotechnology student exploring bioinformatics, computational biology, and the intersection of biology, data, and code.

GitHub: [aadya2909](https://github.com/aadya2909)


