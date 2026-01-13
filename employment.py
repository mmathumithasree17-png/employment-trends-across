import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create sample dataset for Indian states employment data
def create_sample_data():
    """
    Creates sample employment data for Indian states
    Data includes: State, Employment Rate (%), Workforce (in millions), Year
    """
    states = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
        'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
        'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
        'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi', 'Jammu & Kashmir'
    ]
    
    # Generate realistic employment rates (%) and workforce data
    np.random.seed(42)
    employment_rates = np.random.uniform(35, 52, len(states))
    workforce_millions = np.random.uniform(2, 45, len(states))
    
    # Adjust some states to create realistic patterns
    employment_rates[states.index('Goa')] = 51.2
    employment_rates[states.index('Delhi')] = 50.8
    employment_rates[states.index('Kerala')] = 49.5
    employment_rates[states.index('Gujarat')] = 48.9
    employment_rates[states.index('Karnataka')] = 48.2
    
    employment_rates[states.index('Bihar')] = 36.5
    employment_rates[states.index('Jharkhand')] = 37.2
    employment_rates[states.index('Uttar Pradesh')] = 37.8
    employment_rates[states.index('Assam')] = 38.5
    employment_rates[states.index('Madhya Pradesh')] = 39.1
    
    # Adjust workforce for large states
    workforce_millions[states.index('Uttar Pradesh')] = 43.5
    workforce_millions[states.index('Maharashtra')] = 38.2
    workforce_millions[states.index('West Bengal')] = 32.8
    workforce_millions[states.index('Bihar')] = 28.5
    workforce_millions[states.index('Tamil Nadu')] = 26.3
    
    data = pd.DataFrame({
        'State': states,
        'Employment_Rate': np.round(employment_rates, 2),
        'Workforce_Millions': np.round(workforce_millions, 2),
        'Year': 2024
    })
    
    return data

# Load or create the dataset
df = create_sample_data()

# Save to CSV for future use
df.to_csv('indian_states_employment_data.csv', index=False)
print("Sample dataset created and saved as 'indian_states_employment_data.csv'\n")

# Display basic statistics
print("="*70)
print("EMPLOYMENT TRENDS ANALYSIS - INDIAN STATES")
print("="*70)
print("\nDataset Overview:")
print(df.head(10))
print(f"\nTotal States Analyzed: {len(df)}")
print(f"\nBasic Statistics:")
print(df[['Employment_Rate', 'Workforce_Millions']].describe())

# Sort by employment rate
df_sorted = df.sort_values('Employment_Rate', ascending=False)

# Get top 5 and bottom 5 states
top_5 = df_sorted.head(5)
bottom_5 = df_sorted.tail(5)

print("\n" + "="*70)
print("TOP 5 STATES - HIGHEST EMPLOYMENT RATES")
print("="*70)
for idx, row in top_5.iterrows():
    print(f"{row['State']:25s} | Employment Rate: {row['Employment_Rate']:5.2f}% | Workforce: {row['Workforce_Millions']:6.2f}M")

print("\n" + "="*70)
print("BOTTOM 5 STATES - LOWEST EMPLOYMENT RATES")
print("="*70)
for idx, row in bottom_5.iterrows():
    print(f"{row['State']:25s} | Employment Rate: {row['Employment_Rate']:5.2f}% | Workforce: {row['Workforce_Millions']:6.2f}M")

# Calculate regional disparity
disparity = top_5['Employment_Rate'].mean() - bottom_5['Employment_Rate'].mean()
print(f"\n{'='*70}")
print(f"REGIONAL DISPARITY: {disparity:.2f}% (difference between top 5 and bottom 5 average)")
print(f"{'='*70}\n")

# Create visualizations
fig = plt.figure(figsize=(18, 12))

# 1. Bar chart - All states employment rate
ax1 = plt.subplot(2, 3, 1)
colors = ['green' if i < 5 else 'red' if i >= len(df_sorted) - 5 else 'skyblue' 
          for i in range(len(df_sorted))]
ax1.barh(df_sorted['State'], df_sorted['Employment_Rate'], color=colors, alpha=0.7)
ax1.set_xlabel('Employment Rate (%)', fontsize=11, fontweight='bold')
ax1.set_title('Employment Rate Across Indian States\n(Green: Top 5, Red: Bottom 5)', 
              fontsize=12, fontweight='bold')
ax1.axvline(df['Employment_Rate'].mean(), color='black', linestyle='--', 
            linewidth=2, label=f'National Avg: {df["Employment_Rate"].mean():.2f}%')
ax1.legend()
plt.tight_layout()

# 2. Top 5 vs Bottom 5 comparison
ax2 = plt.subplot(2, 3, 2)
comparison_df = pd.concat([top_5, bottom_5])
colors_comp = ['green']*5 + ['red']*5
ax2.bar(range(len(comparison_df)), comparison_df['Employment_Rate'], 
        color=colors_comp, alpha=0.7, edgecolor='black')
ax2.set_xticks(range(len(comparison_df)))
ax2.set_xticklabels(comparison_df['State'], rotation=45, ha='right', fontsize=9)
ax2.set_ylabel('Employment Rate (%)', fontsize=11, fontweight='bold')
ax2.set_title('Top 5 vs Bottom 5 States\nEmployment Rate Comparison', 
              fontsize=12, fontweight='bold')
ax2.axhline(df['Employment_Rate'].mean(), color='black', linestyle='--', 
            linewidth=2, alpha=0.7)
plt.tight_layout()

# 3. Workforce distribution
ax3 = plt.subplot(2, 3, 3)
top_workforce = df.nlargest(10, 'Workforce_Millions')
ax3.barh(top_workforce['State'], top_workforce['Workforce_Millions'], 
         color='coral', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Workforce (Millions)', fontsize=11, fontweight='bold')
ax3.set_title('Top 10 States by Workforce Size', fontsize=12, fontweight='bold')
plt.tight_layout()

# 4. Employment rate distribution histogram
ax4 = plt.subplot(2, 3, 4)
ax4.hist(df['Employment_Rate'], bins=15, color='steelblue', 
         alpha=0.7, edgecolor='black')
ax4.axvline(df['Employment_Rate'].mean(), color='red', linestyle='--', 
            linewidth=2, label=f'Mean: {df["Employment_Rate"].mean():.2f}%')
ax4.axvline(df['Employment_Rate'].median(), color='green', linestyle='--', 
            linewidth=2, label=f'Median: {df["Employment_Rate"].median():.2f}%')
ax4.set_xlabel('Employment Rate (%)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Number of States', fontsize=11, fontweight='bold')
ax4.set_title('Distribution of Employment Rates', fontsize=12, fontweight='bold')
ax4.legend()
plt.tight_layout()

# 5. Scatter plot - Employment rate vs Workforce
ax5 = plt.subplot(2, 3, 5)
scatter = ax5.scatter(df['Workforce_Millions'], df['Employment_Rate'], 
                     s=df['Workforce_Millions']*10, alpha=0.6, 
                     c=df['Employment_Rate'], cmap='RdYlGn', edgecolors='black')
for idx, row in top_5.iterrows():
    ax5.annotate(row['State'], (row['Workforce_Millions'], row['Employment_Rate']),
                fontsize=8, alpha=0.7)
ax5.set_xlabel('Workforce (Millions)', fontsize=11, fontweight='bold')
ax5.set_ylabel('Employment Rate (%)', fontsize=11, fontweight='bold')
ax5.set_title('Employment Rate vs Workforce Size\n(Bubble size = Workforce)', 
              fontsize=12, fontweight='bold')
plt.colorbar(scatter, ax=ax5, label='Employment Rate (%)')
plt.tight_layout()

# 6. Regional disparity visualization
ax6 = plt.subplot(2, 3, 6)
categories = ['Top 5\nStates', 'Middle States', 'Bottom 5\nStates']
middle_states = df_sorted.iloc[5:-5]
avg_rates = [top_5['Employment_Rate'].mean(), 
             middle_states['Employment_Rate'].mean(),
             bottom_5['Employment_Rate'].mean()]
colors_cat = ['green', 'orange', 'red']
bars = ax6.bar(categories, avg_rates, color=colors_cat, alpha=0.7, edgecolor='black')
ax6.set_ylabel('Average Employment Rate (%)', fontsize=11, fontweight='bold')
ax6.set_title('Regional Disparity Analysis\nAverage Employment Rates by Category', 
              fontsize=12, fontweight='bold')
for bar, val in zip(bars, avg_rates):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{val:.2f}%', ha='center', fontweight='bold')
plt.tight_layout()

plt.suptitle('EMPLOYMENT TRENDS ACROSS INDIAN STATES - 2024', 
             fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('indian_employment_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print("✓ Dataset saved: 'indian_states_employment_data.csv'")
print("✓ Visualizations saved: 'indian_employment_analysis.png'")
print("✓ Analysis includes: All states comparison, Top/Bottom 5, Regional disparities")
print("="*70)