import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
#file_path = 'electionsClean.xlsx'
elections_df = pd.read_excel('electionsClean.xlsx')

# Exclude unnecessary rows (like totals or non-vote counts) for cleaner analysis
elections_df = elections_df.drop([52, 55])

# Convert vote counts to numeric
regions = ['Eastern Cape', 'Free State', 'Gauteng', 'KwaZulu-Natal', 'Limpopo', 
           'Mpumalanga', 'North West', 'Northern Cape', 'Western Cape']

for region in regions:
    elections_df[region] = pd.to_numeric(elections_df[region], errors='coerce')

# Function to extract leading digit
def leading_digit(number):
    number = str(number).lstrip('0.')
    return int(number[0]) if number else 0

# Extract leading digits for each region and store in a single series
leading_digits = pd.Series(dtype=int)
for region in regions:
    leading_digits = leading_digits.append(elections_df[region].apply(leading_digit))

# Remove any leading zeros (if present)
leading_digits = leading_digits[leading_digits != 0]

# Compute frequency distribution of leading digits
observed_counts = leading_digits.value_counts().sort_index()
observed_freq = observed_counts / observed_counts.sum()

# Benford's expected distribution
benford_freq = [np.log10(1 + 1/d) for d in range(1, 10)]

# Plot observed vs. expected frequencies
plt.figure(figsize=(10, 6))
plt.bar(observed_freq.index, observed_freq, alpha=0.7, label='Observed', color='blue')
plt.plot(range(1, 10), benford_freq, 'r-', marker='o', label='Benford\'s Law', color='red')
plt.xlabel('Leading Digit')
plt.ylabel('Frequency')
plt.title('Leading Digit Distribution vs. Benford\'s Law')
plt.legend()
plt.show()
