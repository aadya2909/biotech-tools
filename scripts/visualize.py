import matplotlib.pyplot as plt
from src.ncbi.fetch import fetch_gene
from src.ncbi.search import search_gene

def plot_gc_content(gene_names):
    genes = []
    gc_values = []

    for gene_name in gene_names:
        print(f"Fetching {gene_name}...")
        gene_id = search_gene(gene_name)
        if gene_id:
            record = fetch_gene(gene_id)
            sequence = str(record.seq).upper()
            gc = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
            genes.append(gene_name)
            gc_values.append(round(gc, 2))
            print(f"{gene_name}: {round(gc, 2)}%")
        else:
            print(f"{gene_name}: not found")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')

    colors = ['#58a6ff', '#3fb950', '#f78166', '#d2a8ff', '#ffa657']
    bars = ax.bar(genes, gc_values, color=colors, edgecolor='none', width=0.5)

    ax.set_title("GC Content Across Cancer Genes", fontsize=16,
                 fontweight='bold', color='white', pad=20)
    ax.set_xlabel("Gene", fontsize=12, color='#8b949e', labelpad=10)
    ax.set_ylabel("GC Content (%)", fontsize=12, color='#8b949e', labelpad=10)
    ax.set_ylim(0, 80)

    ax.tick_params(colors='#8b949e', labelsize=11)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.yaxis.grid(True, color='#21262d', linewidth=0.8)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, gc_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val}%", ha='center', fontsize=11,
                color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig("data/gc_content_comparison.png", dpi=150,
                facecolor='#0d1117', bbox_inches='tight')
    print("\nChart saved to data/gc_content_comparison.png")

if __name__ == "__main__":
    plot_gc_content(["TP53", "BRCA1", "KRAS", "EGFR", "MYC"])