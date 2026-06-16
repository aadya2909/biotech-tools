# Bioinformatics Concepts Used in This Project

This document explains the main biological and computational concepts used in `biotech-tools`.

## RefSeq mRNA records

The pipeline filters for RefSeq `NM_` accessions because they represent curated messenger RNA records. These records are more reliable for gene-level analysis than random nucleotide fragments, predicted sequences, or unreviewed records.

Example:

```text
NM_001407264.1
```

In this project, RefSeq mRNA records are used as the main sequence source for analysis.

## FASTA format

FASTA is a simple text format used to store biological sequences.

A FASTA record has two parts:

```text
>sequence_identifier
ATGCATGCATGC
```

The first line begins with `>` and stores the sequence identifier.
The following lines contain the nucleotide or protein sequence.

In this project, fetched nucleotide sequences are saved as `.fasta` files inside the `data/` directory.

## GC content

GC content measures the percentage of guanine and cytosine bases in a DNA or RNA sequence.

```text
GC content = (G + C) / total sequence length × 100
```

GC content can vary between genes and may be useful for comparing sequence composition.

## Start and stop codons

A start codon usually marks the beginning of protein translation.

```text
ATG
```

Stop codons signal the end of translation.

```text
TAA
TAG
TGA
```

This project scans sequences for start and stop codon positions as part of basic sequence analysis.

## Open Reading Frame

An open reading frame, or ORF, is a stretch of nucleotide sequence that begins with a start codon and continues until a stop codon is reached.

Earlier versions of this project used the longest ORF as a simple way to estimate a protein sequence.

This is useful for learning, but it is not always biologically accurate for mutation-position analysis.

## CDS

CDS stands for coding sequence.

A CDS is the annotated region of a gene transcript that is translated into protein. GenBank records often include CDS features that contain the official protein translation.

This project now extracts the annotated CDS protein from GenBank records when available.

This is more accurate than relying only on the longest ORF.

## Longest ORF vs annotated CDS

The longest ORF is computationally guessed from the raw sequence.

The annotated CDS is curated biological information from the GenBank record.

For mutation analysis, annotated CDS protein is preferred because mutation positions must match the correct protein coordinates.

Example:

```text
Longest ORF protein length: 407 aa
Annotated CDS protein length: 393 aa
```

Using the annotated CDS protein helps avoid false “different variant” results caused by incorrect protein alignment.

## Mutation notation

A mutation such as `R175H` means:

```text
R = original amino acid
175 = position in the protein
H = mutated amino acid
```

So `R175H` means arginine at position 175 is replaced by histidine.

In this project, known mutation sites are checked against the extracted protein sequence.

## Mutation report

The mutation report summarizes:

* gene name
* protein length
* known mutation sites checked
* expected amino acid
* observed amino acid
* mutation status
* mutation type
* short biological note

The report is saved in the `reports/` directory.

## CSV summary

The CSV summary provides structured output for multiple genes.

Example fields:

```text
gene
sequence_length
protein_length
protein_source
gc_content
known_sites_checked
mutations_detected
different_variants
```

This makes the output easier to compare, analyze, or visualize later.

## Project limitation

This project is educational and research-oriented.

It does not analyze patient sequencing data, perform clinical diagnosis, predict disease, recommend treatment, or replace professional medical interpretation.
