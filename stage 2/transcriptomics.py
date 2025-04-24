import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import time

# Step 1: Load and fix the dataset
url = "https://gist.githubusercontent.com/stephenturner/806e31fce55a8b7175af/raw/1a507c4c3f9f1baaa3a69187223ff3d3050628d4/results.txt"
df = pd.read_csv(url, delim_whitespace=True)  # Use whitespace as delimiter

# Step 2: Prepare data for volcano plot
df['neg_log10_pvalue'] = -np.log10(df['pvalue'])

# Step 3: Volcano Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='log2FoldChange', y='neg_log10_pvalue',
                hue=(df['log2FoldChange'].abs() > 1) & (df['pvalue'] < 0.01),
                palette={True: 'red', False: 'gray'}, edgecolor=None, alpha=0.6)
plt.axvline(1, color='black', linestyle='--')
plt.axvline(-1, color='black', linestyle='--')
plt.axhline(-np.log10(0.01), color='blue', linestyle='--')
plt.title("Volcano Plot")
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(p-value)")
plt.legend(['Thresholds', 'Significant'], loc='upper right')
plt.tight_layout()
plt.grid(True)
plt.show()

# Step 4: Identify top upregulated and downregulated genes
upregulated = df[(df['log2FoldChange'] > 1) & (df['pvalue'] < 0.01)]
downregulated = df[(df['log2FoldChange'] < -1) & (df['pvalue'] < 0.01)]

top_up = upregulated.sort_values('log2FoldChange', ascending=False).head(5)
top_down = downregulated.sort_values('log2FoldChange').head(5)

# Step 5: Scrape gene functions from GeneCards
def fetch_gene_function(gene_name):
    base_url = f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        summary_section = soup.find('div', id='summaries')
        if summary_section:
            paragraphs = summary_section.find_all('p')
            for para in paragraphs:
                text = para.get_text(strip=True)
                if text:
                    return text
        return "Function description not found."
    except Exception as e:
        return f"Error fetching data: {e}"

# Step 6: Combine and fetch gene functions
combined = pd.concat([top_up, top_down], ignore_index=True)
functions = []

for gene in combined['gene']:
    print(f"Fetching function for {gene}...")
    desc = fetch_gene_function(gene)
    functions.append({'Gene': gene, 'Function': desc})
    time.sleep(1)  # Be polite to GeneCards server

# Step 7: Save to CSV
function_df = pd.DataFrame(functions)
function_df.to_csv("top_gene_functions.csv", index=False)
print("Saved gene functions to 'top_gene_functions.csv'")
