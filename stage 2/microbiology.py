#start coding... 
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Load growth data
growth_url = "https://raw.githubusercontent.com/HackBio-Internship/2025_project_collection/refs/heads/main/Python/Dataset/mcgc.tsv"
growth_df = pd.read_csv(growth_url, sep="\t")

# Load and parse metadata
meta_url = "https://raw.githubusercontent.com/HackBio-Internship/2025_project_collection/main/Python/Dataset/mcgc_METADATA.txt"
meta_txt = requests.get(meta_url).text.strip().splitlines()

meta_header = meta_txt[0].split()
meta_list = []

for line in meta_txt[1:]:
    parts = line.split()
    strain, rep = parts[0].split('_')
    wells = parts[1:]
    for i, genotype in enumerate(meta_header[1:]):  # ['WT', 'MUT']
        meta_list.append({
            'Well': wells[i],
            'Strain': strain,
            'Genotype': genotype,
            'Replicate': rep
        })

# Create DataFrame
meta_df = pd.DataFrame(meta_list)

# Melt growth data to long format
long_df = growth_df.melt(id_vars='time', var_name='Well', value_name='OD600')

# Merge with metadata
merged_df = pd.merge(long_df, meta_df, on='Well')

# ✅ Plot one figure per strain
for strain in merged_df['Strain'].unique():
    strain_data = merged_df[merged_df['Strain'] == strain]
    
    plt.figure(figsize=(8, 5))
    
    for genotype in ['WT', 'MUT']:
        gen_data = strain_data[strain_data['Genotype'] == genotype]
        for rep in gen_data['Replicate'].unique():
            rep_data = gen_data[gen_data['Replicate'] == rep]
            label = f"{genotype} - Rep {rep}"
            plt.plot(rep_data['time'], rep_data['OD600'], label=label)
    
    plt.title(f"Growth Curve - {strain}")
    plt.xlabel("Time (minutes)")
    plt.ylabel("OD600")
    plt.legend()
    plt.tight_layout()
    plt.show()

from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------------------
# ✅ Compute time to carrying capacity for each curve
# -----------------------------------------------
carrying_cap_data = []

# Group by each unique growth curve (Strain + Replicate + Genotype)
grouped = merged_df.groupby(['Strain', 'Replicate', 'Genotype'])

for (strain, rep, genotype), group in grouped:
    group_sorted = group.sort_values('time')
    max_od = group_sorted['OD600'].max()
    threshold = 0.95 * max_od  # Define carrying capacity as 95% of max OD
    
    # Find the first time OD600 reaches 95% of max
    reached = group_sorted[group_sorted['OD600'] >= threshold]
    if not reached.empty:
        time_to_capacity = reached.iloc[0]['time']
        carrying_cap_data.append({
            'Strain': strain,
            'Replicate': rep,
            'Genotype': genotype,
            'TimeToCapacity': time_to_capacity
        })

# Put results in a DataFrame
capacity_df = pd.DataFrame(carrying_cap_data)

# -----------------------------------------------
# ✅ Scatter Plot: time to carrying capacity
# -----------------------------------------------
plt.figure(figsize=(8, 5))
sns.stripplot(data=capacity_df, x='Genotype', y='TimeToCapacity', jitter=True, palette='Set2')
plt.title("Time to Reach Carrying Capacity (Scatter Plot)")
plt.xlabel("Genotype")
plt.ylabel("Time (minutes)")
plt.grid(True)
plt.tight_layout()
plt.show()


#  Box Plot: time to carrying capacity

plt.figure(figsize=(8, 5))
sns.boxplot(data=capacity_df, x='Genotype', y='TimeToCapacity', palette='Set2')
plt.title("Time to Reach Carrying Capacity (Box Plot)")
plt.xlabel("Genotype")
plt.ylabel("Time (minutes)")
plt.grid(True)
plt.tight_layout()
plt.show()


#  Statistical Test: t-test (WT vs MUT)

wt_times = capacity_df[capacity_df['Genotype'] == 'WT']['TimeToCapacity']
mut_times = capacity_df[capacity_df['Genotype'] == 'MUT']['TimeToCapacity']

t_stat, p_value = ttest_ind(wt_times, mut_times, equal_var=False)

print(f"\nStatistical Test Result (t-test):")
print(f"T-statistic = {t_stat:.3f}")
print(f"P-value = {p_value:.4f}")


# Interpret observations as comments


# ▶️ Observation:
# The scatter and box plots show the spread and central tendency of time to carrying capacity
# between knock-in (WT) and knock-out (MUT) strains.
#
# ▶️ If p-value < 0.05:
# This suggests a statistically significant difference — i.e., knock-outs may take longer or shorter
# to reach carrying capacity than the wild type, depending on gene impact.
#
# ▶️ Biological Insight:
# A slower time to capacity in MUT might indicate that the gene knocked out plays a role in growth or metabolism.
# Faster capacity in MUT could suggest the gene suppresses growth or that knock-in strains experience some burden.
