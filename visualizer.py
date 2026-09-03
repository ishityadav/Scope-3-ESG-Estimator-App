import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def generate_dashboard(benchmark_df, master_df):
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # -------------------------------------------------------------
    # Panel 1: Benchmark (Absolute Emissions vs Carbon Intensity)
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    x = np.arange(len(benchmark_df['Company']))
    width = 0.35

    ax1.bar(x, benchmark_df['Emissions_tCO2e'] / 1e6, width, color='#2c3e50', label='Emissions (Million tCO2e)')
    ax1.set_ylabel('Scope 3 Emissions (Million tCO2e)', color='#2c3e50', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(benchmark_df['Company'], fontweight='bold')
    ax1.set_title('1. Corporate Benchmark: Scale vs Efficiency', fontsize=12, fontweight='bold', pad=10)

    ax1_twin = ax1.twinx()
    ax1_twin.plot(x, benchmark_df['Carbon_Intensity (tCO2e/Cr_Rev)'], color='#e74c3c', marker='o', linewidth=2.5, markersize=8)
    ax1_twin.set_ylabel('Intensity (tCO2e / ₹1 Cr Revenue)', color='#e74c3c', fontweight='bold')
    ax1_twin.grid(False)

    # -------------------------------------------------------------
    # Panel 2: Stacked Scope 3 Category Breakdown
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    pivot_cat = master_df.pivot_table(
        index='Company', 
        columns='GHG_Scope3_Category', 
        values='Emissions_tCO2e', 
        aggfunc='sum'
    ).fillna(0) / 1e3  # in thousand tCO2e

    pivot_cat.plot(kind='bar', stacked=True, ax=ax2, colormap='Spectral', edgecolor='black', linewidth=0.5)
    ax2.set_title('2. Scope 3 Emissions by GHG Protocol Category', fontsize=12, fontweight='bold', pad=10)
    ax2.set_ylabel('Emissions (Thousand tCO2e)', fontweight='bold')
    ax2.set_xlabel('')
    ax2.tick_params(axis='x', rotation=0)
    ax2.legend(title='Category', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)

    # -------------------------------------------------------------
    # Panel 3: ITC Limited Category % Distribution (Donut Chart)
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    itc_data = master_df[master_df['Company'] == 'ITC Limited'].groupby('GHG_Scope3_Category')['Emissions_tCO2e'].sum()
    colors = sns.color_palette('pastel')[0:len(itc_data)]
    
    wedges, texts, autotexts = ax3.pie(
        itc_data, 
        labels=None, 
        autopct='%1.1f%%', 
        pctdistance=0.75, 
        colors=colors,
        startangle=140
    )
    centre_circle = plt.Circle((0, 0), 0.55, fc='white')
    ax3.add_artist(centre_circle)
    ax3.set_title('3. ITC Limited Footprint Share (%)', fontsize=12, fontweight='bold', pad=10)
    ax3.legend(wedges, itc_data.index, title="Categories", loc="center left", bbox_to_anchor=(0.9, 0.5), fontsize=8)

    # -------------------------------------------------------------
    # Panel 4: Spend vs Emissions Disparity (Pareto Insight)
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    spend_vs_emit = master_df.groupby('Expense_Item')[['Spend_INR_Crores', 'Emissions_tCO2e']].sum().reset_index()
    spend_vs_emit['% Spend'] = (spend_vs_emit['Spend_INR_Crores'] / spend_vs_emit['Spend_INR_Crores'].sum()) * 100
    spend_vs_emit['% Emissions'] = (spend_vs_emit['Emissions_tCO2e'] / spend_vs_emit['Emissions_tCO2e'].sum()) * 100
    spend_vs_emit = spend_vs_emit.sort_values(by='% Emissions', ascending=False)

    y_pos = np.arange(len(spend_vs_emit))
    bar_h = 0.35

    ax4.barh(y_pos - bar_h/2, spend_vs_emit['% Spend'], bar_h, label='% Total Spend', color='#3498db')
    ax4.barh(y_pos + bar_h/2, spend_vs_emit['% Emissions'], bar_h, label='% Total Carbon Footprint', color='#e67e22')
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(spend_vs_emit['Expense_Item'], fontsize=9)
    ax4.set_xlabel('Share of Total (%)', fontweight='bold')
    ax4.set_title('4. Procurement Spend vs Carbon Impact Distribution', fontsize=12, fontweight='bold', pad=10)
    ax4.legend(loc='lower right')

    plt.tight_layout()
    plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
    print("\n✓ Full 4-panel executive dashboard saved to 'executive_dashboard.png'")