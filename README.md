# biotech-tools

A Python-based bioinformatics pipeline for gene sequence analysis, 
mutation detection, and protein translation using real NCBI data.

## What this project does

I built this to learn how computational biology actually works — 
not just theory. Starting from raw gene names, the pipeline fetches 
real sequences from NCBI, analyzes nucleotide composition, detects 
known cancer mutations at the amino acid level, and translates DNA 
to protein. Everything here is built and understood from scratch.

## Project structure

biotech-tools/
├── data/                # FASTA files fetched from NCBI
├── scripts/
│   ├── fetch_gene.py    # Fetches any gene from NCBI by name
│   ├── analyze.py       # Full sequence analysis + protein translation
│   ├── p53_analyzer.py  # TP53 tumor suppressor gene analysis
│   └── kras_analyzer.py # KRAS oncogene mutation detection
├── src/ncbi/
│   ├── fetch.py         # NCBI fetch functions
│   └── search.py        # NCBI search functions
└── requirements.txt

## Installation

pip install -r requirements.txt

## Usage

Fetch any gene from NCBI:
python -m scripts.fetch_gene

Run full sequence analysis:
python -m scripts.analyze

Run KRAS cancer mutation analysis:
python -m scripts.kras_analyzer

## Example output

Gene: PZ086170.1
Length: 123 bp
Nucleotide counts — A: 23, T: 20, G: 35, C: 45
GC Content: 65.04%
Start codons found: 2 at positions [69, 100]
Protein: WVDSTPPPGTRVRAVAIYKQSQHMTEVVRRCPHHERCSDSD

## Author

Aadya | BSc Biotechnology student  
Building at the intersection of biology and code  
github.com/aadya2909