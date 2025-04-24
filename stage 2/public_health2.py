#start coding... 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load dataset
url = "https://raw.githubusercontent.com/HackBio-Internship/public_datasets/main/R/nhanes.csv"
df = pd.read_csv(url)


# 1. Handle Missing Values

# Option 1 (delete NA rows): df = df.dropna()
# Option 2 (replace NA with 0):
df.fillna(0, inplace=True)


# 2. Histograms

df['Weight_lb'] = df['Weight'] * 2.2  # Convert weight to pounds

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
sns.histplot(df['BMI'], kde=True, bins=30, color='blue')
plt.title('BMI Distribution')

plt.subplot(2, 2, 2)
sns.histplot(df['Weight'], kde=True, bins=30, color='green')
plt.title('Weight (kg) Distribution')

plt.subplot(2, 2, 3)
sns.histplot(df['Weight_lb'], kde=True, bins=30, color='purple')
plt.title('Weight (lbs) Distribution')

plt.subplot(2, 2, 4)
sns.histplot(df['Age'], kde=True, bins=30, color='orange')
plt.title('Age Distribution')

plt.tight_layout()
plt.show()


#  3. Summary Statistics

# Mean pulse rate
mean_pulse = df['Pulse'].mean()
print(f"Mean 60-second pulse rate: {mean_pulse:.5f}")  # Should match 73.63382

# Range of Diastolic BP
min_dia = df['BPDia'].min()
max_dia = df['BPDia'].max()
print(f"Range of Diastolic Blood Pressure: {min_dia} - {max_dia}")

# Variance and SD of Income
income_var = df['Income'].var()
income_std = df['Income'].std()
print(f"Income Variance: {income_var:.2f}")
print(f"Income Standard Deviation: {income_std:.2f}")


# 4. Weight vs Height scatter

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Height', y='Weight', hue='Gender')
plt.title("Weight vs Height Colored by Gender")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Height', y='Weight', hue='Diabetes')
plt.title("Weight vs Height Colored by Diabetes")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Height', y='Weight', hue='SmokingStatus')
plt.title("Weight vs Height Colored by Smoking Status")
plt.grid(True)
plt.show()


# 5. T-Tests

# a) Age and Gender
age_male = df[df['Gender'] == 'Male']['Age']
age_female = df[df['Gender'] == 'Female']['Age']
t1, p1 = stats.ttest_ind(age_male, age_female)
print(f"\nT-Test: Age vs Gender\nP-Value: {p1:.5f}")
if p1 < 0.05:
    print("✅ Statistically significant difference in Age between genders.")
else:
    print("❌ No significant difference in Age between genders.")

# b) BMI and Diabetes
bmi_diab = df[df['Diabetes'] == 'Yes']['BMI']
bmi_nodiab = df[df['Diabetes'] == 'No']['BMI']
t2, p2 = stats.ttest_ind(bmi_diab, bmi_nodiab)
print(f"\nT-Test: BMI vs Diabetes\nP-Value: {p2:.5f}")
if p2 < 0.05:
    print("✅ Statistically significant difference in BMI for diabetics vs non-diabetics.")
else:
    print("❌ No significant difference in BMI for diabetics.")

# c) Alcohol Year and Relationship Status
alc_single = df[df['RelationshipStatus'] == 'Single']['AlcoholYear']
alc_married = df[df['RelationshipStatus'] == 'Partnered']['AlcoholYear']
t3, p3 = stats.ttest_ind(alc_single, alc_married)
print(f"\nT-Test: AlcoholYear vs RelationshipStatus\nP-Value: {p3:.5f}")
if p3 < 0.05:
    print("✅ Statistically significant difference in alcohol consumption based on relationship status.")
else:
    print("❌ No significant difference in alcohol consumption between groups.")
